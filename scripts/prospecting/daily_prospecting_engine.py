from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[2]
PIPELINE_DIR = ROOT / "pipeline" / "prospecting"
PROSPECT_TRACKER = PIPELINE_DIR / "prospect-tracker.csv"
DAILY_QUEUE = PIPELINE_DIR / "daily-outreach-queue.csv"
RUNS_DIR = PIPELINE_DIR / "runs"

ENV_PATHS = [
    ROOT / ".env",
    Path(r"C:\Users\ELITEX21012G2\bridgeworks-agency\.env.local"),
]

GOOGLE_PLACES_TEXT_SEARCH = "https://maps.googleapis.com/maps/api/place/textsearch/json"
GOOGLE_PLACES_DETAILS = "https://maps.googleapis.com/maps/api/place/details/json"
GOOGLE_PLACES_TEXT_SEARCH_NEW = "https://places.googleapis.com/v1/places:searchText"
FIRECRAWL_SCRAPE = "https://api.firecrawl.dev/v1/scrape"
FIRECRAWL_SEARCH = "https://api.firecrawl.dev/v1/search"
HUNTER_DOMAIN_SEARCH = "https://api.hunter.io/v2/domain-search"
TOMBA_DOMAIN_SEARCH = "https://api.tomba.io/v1/domain-search"


DEFAULT_QUERIES = [
    ("facility management company Lagos official website", "Africa/Nigeria", "Facility management"),
    ("commercial cleaning company Lagos official website", "Africa/Nigeria", "Commercial cleaning"),
    ("property management company Lagos official website", "Africa/Nigeria", "Property management"),
    ("facility management company Abuja official website", "Africa/Nigeria", "Facility management"),
    ("serviced apartment operator London official website", "UK/EU", "Serviced apartments"),
    ("property management company London official website", "UK/EU", "Property management"),
    ("facility management company Warsaw official website", "CEE", "Facility management"),
    ("property management company Warsaw official website", "CEE", "Property management"),
    ("facility management company Prague official website", "CEE", "Facility management"),
    ("serviced apartment operator Prague official website", "CEE", "Serviced apartments"),
]

BLOCKED_DISCOVERY_HOSTS = {
    "google.com",
    "www.google.com",
    "linkedin.com",
    "www.linkedin.com",
    "facebook.com",
    "www.facebook.com",
    "instagram.com",
    "www.instagram.com",
    "x.com",
    "twitter.com",
    "ng.linkedin.com",
    "uk.linkedin.com",
    "pl.linkedin.com",
}

BLOCKED_TITLE_WORDS = [
    "association of",
    "directory",
    "yellow pages",
    "facebook",
    "instagram",
    "linkedin",
    "jobs",
    "career",
    "wikipedia",
]

FIELDNAMES = [
    "id",
    "date_added",
    "campaign",
    "market",
    "niche",
    "company",
    "website",
    "city",
    "country",
    "contact_name",
    "contact_role",
    "email",
    "linkedin",
    "source",
    "source_tool",
    "skill_used",
    "signal_found",
    "growth_leak",
    "offer_fit",
    "recommended_service",
    "estimated_value",
    "priority_score",
    "priority",
    "status",
    "next_action_date",
    "outreach_angle",
    "message_1",
    "follow_up_1",
    "follow_up_2",
    "gmail_draft_id",
    "last_contacted_date",
    "reply_status",
    "notes",
]


@dataclass
class Candidate:
    company: str
    website: str
    city: str
    country: str
    market: str
    niche: str
    source: str
    source_tool: str
    rating: str = ""
    review_count: str = ""
    phone: str = ""
    place_url: str = ""


def load_env() -> dict[str, str]:
    values: dict[str, str] = {}
    for path in ENV_PATHS:
        if not path.exists():
            continue
        for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip().lstrip("\ufeff")
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value
            values[key] = value
    return values


def env_presence(env: dict[str, str]) -> dict[str, bool]:
    keys = [
        "GOOGLE_PLACES_API_KEY",
        "GOOGLE_API_KEY",
        "FIRECRAWL_API_KEY",
        "APIFY_API_KEY",
        "HUNTER_API_KEY",
        "TOMBA_API_KEY",
        "TOMBA_SECRET_KEY",
        "SERPAPI_API_KEY",
        "APOLLO_API_KEY",
        "GEMINI_API_KEY",
        "ANTHROPIC_API_KEY",
    ]
    return {key: bool(env.get(key) or os.environ.get(key)) for key in keys}


def request_json(
    url: str,
    *,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    payload: dict[str, Any] | None = None,
    timeout: int = 30,
) -> dict[str, Any]:
    body = None
    final_headers = {"User-Agent": "BridgeWorksProspecting/1.0"}
    if headers:
        final_headers.update(headers)
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        final_headers["Content-Type"] = "application/json"
    req = Request(url, data=body, method=method, headers=final_headers)
    with urlopen(req, timeout=timeout) as response:
        raw = response.read().decode("utf-8", errors="replace")
    return json.loads(raw)


def normalize_domain(url: str) -> str:
    if not url:
        return ""
    parsed = urlparse(url if "://" in url else f"https://{url}")
    host = parsed.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    return host


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    tmp.replace(path)


def next_prospect_id(rows: list[dict[str, str]]) -> int:
    max_id = 0
    for row in rows:
        match = re.search(r"P-(\d+)", row.get("id", ""))
        if match:
            max_id = max(max_id, int(match.group(1)))
    return max_id + 1


def known_domains(rows: list[dict[str, str]]) -> set[str]:
    domains: set[str] = set()
    for row in rows:
        domain = normalize_domain(row.get("website", ""))
        if domain:
            domains.add(domain)
    return domains


def split_location(formatted_address: str, fallback_market: str) -> tuple[str, str]:
    parts = [part.strip() for part in formatted_address.split(",") if part.strip()]
    if len(parts) >= 2:
        return parts[-2], parts[-1]
    if "Nigeria" in fallback_market:
        return "", "Nigeria"
    if fallback_market == "UK/EU":
        return "", "United Kingdom"
    if fallback_market == "CEE":
        return "", "CEE"
    return "", ""


def google_places_candidates(query: str, market: str, niche: str, limit: int) -> tuple[list[Candidate], str]:
    api_key = os.environ.get("GOOGLE_PLACES_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return [], "missing_key"

    new_candidates, new_status = google_places_new_candidates(query, market, niche, limit, api_key)
    if new_candidates or new_status in {"OK", "ZERO_RESULTS"}:
        return new_candidates, f"new:{new_status}"

    try:
        params = urlencode({"query": query, "key": api_key})
        data = request_json(f"{GOOGLE_PLACES_TEXT_SEARCH}?{params}", timeout=30)
        status = data.get("status", "UNKNOWN")
        if status not in {"OK", "ZERO_RESULTS"}:
            return [], f"legacy:{status}"
        results = data.get("results", [])[:limit]
        candidates: list[Candidate] = []
        for item in results:
            place_id = item.get("place_id")
            if not place_id:
                continue
            details_params = urlencode(
                {
                    "place_id": place_id,
                    "fields": "name,website,formatted_address,international_phone_number,url,rating,user_ratings_total",
                    "key": api_key,
                }
            )
            details = request_json(f"{GOOGLE_PLACES_DETAILS}?{details_params}", timeout=30).get("result", {})
            website = details.get("website") or ""
            if not website:
                continue
            city, country = split_location(details.get("formatted_address", ""), market)
            candidates.append(
                Candidate(
                    company=details.get("name") or item.get("name") or "",
                    website=website,
                    city=city,
                    country=country,
                    market=market,
                    niche=niche,
                    source=query,
                    source_tool="Google Places API",
                    rating=str(details.get("rating") or ""),
                    review_count=str(details.get("user_ratings_total") or ""),
                    phone=details.get("international_phone_number") or "",
                    place_url=details.get("url") or "",
                )
            )
            time.sleep(0.1)
        return candidates, f"legacy:{status}"
    except HTTPError as exc:
        return [], f"legacy:HTTP_{exc.code}"
    except URLError:
        return [], "legacy:URLError"
    except TimeoutError:
        return [], "legacy:TimeoutError"
    except json.JSONDecodeError:
        return [], "legacy:JSONDecodeError"


def google_places_new_candidates(
    query: str,
    market: str,
    niche: str,
    limit: int,
    api_key: str,
) -> tuple[list[Candidate], str]:
    try:
        data = request_json(
            GOOGLE_PLACES_TEXT_SEARCH_NEW,
            method="POST",
            headers={
                "X-Goog-Api-Key": api_key,
                "X-Goog-FieldMask": (
                    "places.id,places.displayName,places.formattedAddress,"
                    "places.websiteUri,places.internationalPhoneNumber,"
                    "places.nationalPhoneNumber,places.rating,places.userRatingCount,"
                    "places.googleMapsUri"
                ),
            },
            payload={"textQuery": query, "maxResultCount": min(max(limit, 1), 20)},
            timeout=30,
        )
    except HTTPError as exc:
        return [], f"HTTP_{exc.code}"
    except URLError:
        return [], "URLError"
    except TimeoutError:
        return [], "TimeoutError"
    except json.JSONDecodeError:
        return [], "JSONDecodeError"

    places = data.get("places", [])
    candidates: list[Candidate] = []
    for place in places:
        website = place.get("websiteUri") or ""
        if not website:
            continue
        display = place.get("displayName") or {}
        company = display.get("text") if isinstance(display, dict) else str(display)
        city, country = split_location(place.get("formattedAddress", ""), market)
        candidates.append(
            Candidate(
                company=company or "",
                website=website,
                city=city,
                country=country,
                market=market,
                niche=niche,
                source=query,
                source_tool="Google Places API New",
                rating=str(place.get("rating") or ""),
                review_count=str(place.get("userRatingCount") or ""),
                phone=place.get("internationalPhoneNumber") or place.get("nationalPhoneNumber") or "",
                place_url=place.get("googleMapsUri") or "",
            )
        )
    return candidates, "OK" if places else "ZERO_RESULTS"


def firecrawl_markdown(url: str, max_chars: int = 7000) -> str:
    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key or not url:
        return ""
    try:
        data = request_json(
            FIRECRAWL_SCRAPE,
            method="POST",
            headers={"Authorization": f"Bearer {api_key}"},
            payload={"url": url, "formats": ["markdown"], "onlyMainContent": True},
            timeout=45,
        )
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
        return ""
    body = data.get("data") or data
    text = body.get("markdown") or body.get("content") or ""
    return text[:max_chars]


def firecrawl_search_candidates(query: str, market: str, niche: str, limit: int) -> tuple[list[Candidate], str]:
    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        return [], "missing_key"
    try:
        data = request_json(
            FIRECRAWL_SEARCH,
            method="POST",
            headers={"Authorization": f"Bearer {api_key}"},
            payload={"query": query, "limit": limit},
            timeout=45,
        )
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        return [], type(exc).__name__

    items = data.get("data") or data.get("results") or []
    candidates: list[Candidate] = []
    for item in items:
        url = item.get("url") or item.get("link") or ""
        title = item.get("title") or ""
        if not url or not title:
            continue
        parsed = urlparse(url)
        host = parsed.netloc.lower()
        title_l = title.lower()
        if host in BLOCKED_DISCOVERY_HOSTS:
            continue
        if any(word in title_l for word in BLOCKED_TITLE_WORDS):
            continue
        city, country = split_location("", market)
        company = re.sub(r"\s*[|-].*$", "", title).strip()
        candidates.append(
            Candidate(
                company=company or title,
                website=f"{parsed.scheme}://{parsed.netloc}" if parsed.scheme and parsed.netloc else url,
                city=city,
                country=country,
                market=market,
                niche=niche,
                source=query,
                source_tool="Firecrawl Search",
            )
        )
    return candidates, "OK"


def enrich_email(domain: str) -> tuple[str, str, str]:
    if not domain:
        return "", "", ""

    hunter_key = os.environ.get("HUNTER_API_KEY")
    if hunter_key:
        try:
            params = urlencode({"domain": domain, "api_key": hunter_key, "limit": 5})
            data = request_json(f"{HUNTER_DOMAIN_SEARCH}?{params}", timeout=25)
            emails = (data.get("data") or {}).get("emails") or []
            for email in emails:
                value = email.get("value") or ""
                if value:
                    first = email.get("first_name") or ""
                    last = email.get("last_name") or ""
                    name = " ".join(part for part in [first, last] if part).strip()
                    role = email.get("position") or ""
                    return value, name, role
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
            pass

    tomba_key = os.environ.get("TOMBA_API_KEY")
    tomba_secret = os.environ.get("TOMBA_SECRET_KEY")
    if tomba_key and tomba_secret:
        try:
            params = urlencode({"domain": domain})
            data = request_json(
                f"{TOMBA_DOMAIN_SEARCH}?{params}",
                headers={"X-Tomba-Key": tomba_key, "X-Tomba-Secret": tomba_secret},
                timeout=25,
            )
            emails = (data.get("data") or {}).get("emails") or data.get("emails") or []
            for email in emails:
                value = email.get("email") or ""
                if value:
                    first = email.get("first_name") or ""
                    last = email.get("last_name") or ""
                    name = " ".join(part for part in [first, last] if part).strip()
                    role = email.get("position") or ""
                    return value, name, role
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
            pass

    return "", "", ""


def score_candidate(candidate: Candidate, page_text: str, email: str) -> tuple[int, str]:
    text = f"{candidate.company} {candidate.niche} {page_text}".lower()
    score = 8
    if any(term in text for term in ["facility", "property", "cleaning", "maintenance", "apartment", "hotel"]):
        score += 3
    if any(term in text for term in ["commercial", "industrial", "residential", "hospitality", "office"]):
        score += 2
    if any(term in text for term in ["quote", "contact", "assessment", "booking", "consultation"]):
        score += 2
    if any(term in text for term in ["client", "review", "trusted", "certified", "years", "portfolio"]):
        score += 2
    if email:
        score += 1
    if candidate.rating and candidate.review_count:
        score += 1
    score = min(score, 20)
    if score >= 16:
        return score, "A"
    if score >= 11:
        return score, "B"
    if score >= 6:
        return score, "C"
    return score, "Reject"


def classify_angle(candidate: Candidate, page_text: str) -> tuple[str, str, str, str]:
    text = page_text.lower()
    if any(term in text for term in ["24/7", "emergency", "booking", "quote", "request"]):
        angle = "Speed-to-lead risk"
        service = "AI Growth Systems Starter"
        offer = "Speed-to-lead plus landing page audit"
        leak = "Pain: urgent or high-intent enquiries may not be routed into a visible follow-up path. Outcome: faster response and clearer conversion tracking."
        return angle, offer, service, leak
    if any(term in text for term in ["certified", "client", "portfolio", "trusted", "years", "review"]):
        angle = "Proof gap"
        service = "AI Audit"
        offer = "Proof and GEO audit"
        leak = "Pain: strong credibility may be under-explained online. Outcome: clearer trust proof that buyers and AI/search tools can understand."
        return angle, offer, service, leak
    if any(term in text for term in ["technology", "smart", "sustainable", "integrated"]):
        angle = "AI visibility gap"
        service = "AI Audit"
        offer = "GEO and positioning audit"
        leak = "Pain: strong positioning can sound generic if the site does not make the operating model concrete. Outcome: clearer category ownership and AI-readable service proof."
        return angle, offer, service, leak
    return (
        "Website conversion leak",
        "Website conversion plus GEO audit",
        "AI Audit",
        "Pain: service breadth may not translate into qualified enquiries. Outcome: clearer buyer paths and a stronger route from visit to conversation.",
    )


def make_row(candidate: Candidate, prospect_id: str, page_text: str, email: str, contact_name: str, role: str) -> dict[str, str]:
    today = dt.date.today()
    next_day = today + dt.timedelta(days=1)
    score, priority = score_candidate(candidate, page_text, email)
    angle, offer_fit, recommended_service, growth_leak = classify_angle(candidate, page_text)
    signal_parts = [candidate.niche, "company"]
    if candidate.rating:
        signal_parts.append(f"rating {candidate.rating}")
    if candidate.review_count:
        signal_parts.append(f"{candidate.review_count} reviews")
    signal_found = f"{candidate.company} appears to be a {', '.join(signal_parts)} with a public website and visible service positioning."
    message = f"Draft a pain-versus-outcome teardown around {angle.lower()} for {candidate.company}."
    return {
        "id": prospect_id,
        "date_added": today.isoformat(),
        "campaign": "Multi-Market Property Services Sprint",
        "market": candidate.market,
        "niche": candidate.niche,
        "company": candidate.company,
        "website": candidate.website,
        "city": candidate.city,
        "country": candidate.country,
        "contact_name": contact_name,
        "contact_role": role,
        "email": email,
        "linkedin": "",
        "source": candidate.source,
        "source_tool": candidate.source_tool,
        "skill_used": "prospecting-department; Firecrawl; Google Places; Hunter/Tomba",
        "signal_found": signal_found,
        "growth_leak": growth_leak,
        "offer_fit": offer_fit,
        "recommended_service": recommended_service,
        "estimated_value": "EUR 500 to 3000",
        "priority_score": str(score),
        "priority": priority,
        "status": "Qualified" if priority != "Reject" else "Rejected",
        "next_action_date": next_day.isoformat(),
        "outreach_angle": angle,
        "message_1": message,
        "follow_up_1": "",
        "follow_up_2": "",
        "gmail_draft_id": "",
        "last_contacted_date": "",
        "reply_status": "",
        "notes": "Added by API-backed daily prospecting engine",
    }


def append_queue(rows: list[dict[str, str]]) -> None:
    queue_rows = read_csv(DAILY_QUEUE)
    fieldnames = list(queue_rows[0].keys()) if queue_rows else [
        "date",
        "prospect_id",
        "company",
        "contact_name",
        "channel",
        "action",
        "message_type",
        "status",
        "scheduled_time",
        "completed_time",
        "result",
        "next_step",
    ]
    existing = {(r.get("date", ""), r.get("prospect_id", ""), r.get("action", "")) for r in queue_rows}
    tomorrow = (dt.date.today() + dt.timedelta(days=1)).isoformat()
    times = ["08:30", "08:45", "09:00", "09:15", "09:30"]
    added = 0
    for row in rows:
        if row.get("priority") != "A":
            continue
        key = (tomorrow, row["id"], "Research and draft")
        if key in existing:
            continue
        queue_rows.append(
            {
                "date": tomorrow,
                "prospect_id": row["id"],
                "company": row["company"],
                "contact_name": row.get("contact_name", ""),
                "channel": "Email" if row.get("email") else "Email/Contact form",
                "action": "Research and draft",
                "message_type": row.get("outreach_angle", ""),
                "status": "Queued",
                "scheduled_time": times[min(added, len(times) - 1)],
                "completed_time": "",
                "result": "",
                "next_step": "Create or review a pain-versus-outcome draft; send only after Emmanuel approves.",
            }
        )
        added += 1
    write_csv(DAILY_QUEUE, queue_rows, fieldnames)


def run(limit: int, per_query: int, dry_run: bool) -> dict[str, Any]:
    env = load_env()
    prospects = read_csv(PROSPECT_TRACKER)
    domains = known_domains(prospects)
    next_id = next_prospect_id(prospects)
    new_rows: list[dict[str, str]] = []
    errors: list[str] = []
    provider_status: dict[str, int] = {}
    discovery_tools: dict[str, int] = {}

    for query, market, niche in DEFAULT_QUERIES:
        if len(new_rows) >= limit:
            break
        try:
            candidates, status = google_places_candidates(query, market, niche, per_query)
            provider_status[f"google:{status}"] = provider_status.get(f"google:{status}", 0) + 1
            if candidates:
                discovery_tools["Google Places API"] = discovery_tools.get("Google Places API", 0) + len(candidates)
            if not candidates:
                candidates, fc_status = firecrawl_search_candidates(query, market, niche, per_query)
                provider_status[f"firecrawl_search:{fc_status}"] = provider_status.get(f"firecrawl_search:{fc_status}", 0) + 1
                if candidates:
                    discovery_tools["Firecrawl Search"] = discovery_tools.get("Firecrawl Search", 0) + len(candidates)
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
            errors.append(f"{query}: {type(exc).__name__}")
            continue
        for candidate in candidates:
            if len(new_rows) >= limit:
                break
            domain = normalize_domain(candidate.website)
            if not domain or domain in domains:
                continue
            page_text = firecrawl_markdown(candidate.website)
            email, contact_name, role = enrich_email(domain)
            row = make_row(candidate, f"P-{next_id:04d}", page_text, email, contact_name, role)
            domains.add(domain)
            new_rows.append(row)
            next_id += 1

    if not dry_run and new_rows:
        all_rows = prospects + new_rows
        fieldnames = list(prospects[0].keys()) if prospects else FIELDNAMES
        for name in FIELDNAMES:
            if name not in fieldnames:
                fieldnames.append(name)
        write_csv(PROSPECT_TRACKER, all_rows, fieldnames)
        append_queue(new_rows)

    summary = {
        "date": dt.datetime.now().isoformat(timespec="seconds"),
        "dry_run": dry_run,
        "env_present": env_presence(env),
        "new_prospects": len(new_rows),
        "new_ids": [row["id"] for row in new_rows],
        "new_companies": [row["company"] for row in new_rows],
        "provider_status": provider_status,
        "discovery_tools": discovery_tools,
        "errors": errors,
    }
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    (RUNS_DIR / f"daily-prospecting-{dt.date.today().isoformat()}.json").write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="BridgeWorks API-backed daily prospecting engine")
    parser.add_argument("--limit", type=int, default=10, help="Maximum prospects to add")
    parser.add_argument("--per-query", type=int, default=3, help="Maximum Google Places results per query")
    parser.add_argument("--dry-run", action="store_true", help="Do not write CSV changes")
    args = parser.parse_args()

    summary = run(limit=args.limit, per_query=args.per_query, dry_run=args.dry_run)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
