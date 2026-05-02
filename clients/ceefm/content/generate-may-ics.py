"""
Generate may-calendar.ics for the CEEFM May 2026 LinkedIn calendar.

Reads post data from this file (hard-coded for clarity), writes a single .ics
the user imports into Google Calendar. English-only descriptions per Victor's
EN-only directive; Hungarian hedge stays in may-calendar.md, not the calendar.

Times: CEST is UTC+2 in May 2026. 9:00 CEST = 07:00 UTC. 12:00 CEST = 10:00
UTC. Post 3 is 8:30 CEST = 06:30 UTC. All events 30 min long.
"""
from pathlib import Path

OUT_PATH = Path(__file__).parent / "may-calendar.ics"


def ics_escape(text: str) -> str:
    return (
        text.replace("\\", "\\\\")
            .replace(",", "\\,")
            .replace(";", "\\;")
            .replace("\n", "\\n")
    )


# (number_label, date, hh_mm_utc, title, type_label, image_brief_short, english_body, hashtags)
EVENTS = [
    ("1", "20260505", "0700", "Pre-Summer FM Checklist", "Company/Service",
     "Flat-lay of summer prep tools (AC remote, drainage tube, light bulb, cleaning cloth, key) on Warm Cream #F5F2EC background, Forest Green #1C3D2A accents.",
     "May in Budapest means one thing for property managers: AC season is two weeks away.\n\nHere is what should already be on your desk:\n\n1. Air conditioning commissioning. Filters cleaned. Refrigerant levels checked. Drainage tested. A unit that fails on the first 30°C day is a unit that costs you 3x to repair urgently.\n\n2. Ventilation deep clean. Winter dust accumulates in supply vents. Tenants notice it within hours of running cooling.\n\n3. Common area summer prep. Doormats out. Window cleaning scheduled. Outdoor furniture inspected. First impressions land hardest in good weather.\n\n4. Water system flush. Cold lines that ran low all winter need to clear before summer demand. This is also a Legionella risk window.\n\n5. Pest control prebook. Flies, mosquitos, rodents follow the heat. Booking now costs 30% less than booking in June.\n\n6. Lighting check before days get long. The bulbs that burned out in March are still out. Tenants stop reporting them.\n\nSkip any of these and you are reactive in June. Every time.\n\nWhat is on your May checklist?\n\noffice@ceefm.eu | +36 30 600 5400",
     "#FacilityManagement #Budapest #PropertyOperations #SummerPrep #PropertyManagement"),

    ("2", "20260506", "0700", "Per-Task to Integrated FM Shift", "Industry Insight",
     "Side-by-side graphic: 5 disconnected vendor boxes vs one CEEFM integrated box. Forest Green and Sage Green on Warm Cream background.",
     "Five years ago, most Budapest property owners hired separately:\n- A cleaning company\n- An HVAC contractor\n- A handyman or maintenance service\n- A security firm\n- A landscaping crew\n\nThat model is breaking.\n\nThree things are pushing the shift:\n\nCoordination cost. Five vendors means five contacts, five contracts, five invoicing cycles, five compliance trails. A property manager spends 20-30% of their week just routing problems to the right vendor.\n\nGap risk. When something falls between scopes (the leak that is also a tile issue, the security incident that also needs cleanup), each vendor blames the others. The owner pays anyway.\n\nReporting. Owners who answer to investors or boards now expect integrated metrics. Cleaning frequency, energy consumption, maintenance tickets, compliance status. One report, not five spreadsheets.\n\nIntegrated FM contracts in CEE are growing 7% a year. They are not cheaper per line item. They are cheaper end to end.\n\nThe question to ask is not \"what does each vendor charge?\" It is \"what does this building actually cost to run?\"",
     "#FacilityManagement #IntegratedFM #PropertyOperations #Budapest #FMOutsourcing"),

    ("3", "20260507", "0630", "What a Quality Check Looks Like", "Team/Culture",
     "Corridor walkthrough perspective with clipboard/tablet in lower frame. Soft natural light. Optionally a real CEEFM supervisor portrait if Victor provides one.",
     "At CEEFM, every supervised property gets a quality check at least once a week.\n\nHere is what that actually looks like:\n\nThe supervisor arrives unannounced. Always.\n\nFirst stop is the lobby. Floor reflection at 1.5 meters out from the entrance. Not the whole floor. The first impression zone.\n\nThen the bathroom of the first room or common area. The mirror at chest height. The drain. The toilet rim under the seat. Three points. If any are off, the entire space gets rechecked.\n\nThe supervisor walks the corridor without speaking to staff yet. They are looking for things you only notice when you are not invited: scuff marks at door bases, cobwebs in ceiling corners, dust on top of door frames.\n\nOnly then does the conversation with the on-site team start. With specifics. Not \"good job today.\" Not \"this is wrong.\"\n\n\"Door 3B base needs attention. Schedule it for Thursday.\"\n\nA quality check is not a confrontation. It is a calibration.\n\nDone weekly, it keeps standards from drifting. Skipped for a month, drift becomes habit.\n\nThe buildings we manage do not fall behind because we never let them.",
     "#FacilityManagement #PropertyOperations #Budapest #QualityControl #PropertyManagement"),

    ("F1", "20260508", "1000", "Q2 FM Frustration Poll", "Amplification (Poll)",
     "Native LinkedIn poll - no image required. Optional fallback card with the question text in Forest Green on Warm Cream.",
     "What is your biggest facility management frustration this quarter?\n\n→ Coordinating multiple vendors\n→ Rising energy and material costs\n→ Compliance and reporting workload\n→ Quality drift between site visits\n\nComment if it is something else. We are reading every reply this month.",
     "#FacilityManagement #Budapest #PropertyOperations"),

    ("4", "20260512", "0700", "Vendor Consolidation Math", "Industry Insight",
     "Bar chart: 5 stacked vendor segments (380k+180k+120k+220k+90k=990k visible, translucent extension to 1.25-1.4M) vs single 1.02M integrated bar. Forest Green for integrated, Gray for vendors.",
     "A 60-unit Budapest apartment building running 5 separate vendors typically pays:\n\nCleaning: 380,000 HUF / month\nHVAC and plumbing (callout-based): 180,000 HUF average / month\nGeneral maintenance handyman: 120,000 HUF / month\nSecurity: 220,000 HUF / month\nLandscaping: 90,000 HUF seasonal average / month\n\nDirect line item total: 990,000 HUF.\n\nIndirect costs that nobody itemizes:\n- Property manager time routing requests: 8-12 hours / week\n- Emergency premiums on after-hours callouts: 35% surcharge\n- Materials marked up 20-40% by individual contractors\n- Compliance gaps when a vendor misses a quarterly audit\n- Insurance premium increases when claims trace to vendor confusion\n\nAdd those up honestly and the same building runs 1.25M to 1.4M HUF / month all-in.\n\nAn integrated FM contract for that property type starts at around 1.02M HUF / month with everything included. Consolidated reporting. Single point of accountability. 24/7 coverage at one rate.\n\nThe line items look more expensive on a per-task comparison. The full picture says otherwise.\n\nIf you have not run the math on your building lately, run it.",
     "#FacilityManagement #IntegratedFM #PropertyOperations #Budapest #FMOutsourcing"),

    ("5", "20260513", "0700", "11-Minute 4-Star vs 5-Star Difference", "Company/Service",
     "Close-up of perfectly made hotel bed: tight linens, aligned pillows, hospital corners. Small overlay timestamp +11 min/+11 perc.",
     "A 4-star hotel room takes our team about 22 minutes to clean.\nA 5-star room takes 33 minutes.\n\nWhere do those 11 minutes go?\n\nBathroom: +4 minutes. The 5-star check covers shower glass at three angles, grout in the corners, the underside of the toilet rim, faucet bases. The 4-star check covers visible surfaces.\n\nBed: +2 minutes. Hospital corners. A pillow alignment that holds when a guest sits on the bed. Sheet tension that does not loosen overnight.\n\nSurfaces: +2 minutes. Lampshade tops. The frame edges of artwork. The remote control underside. Surfaces guests touch but never see.\n\nGlassware and minibar: +2 minutes. Every glass is rinsed and polished individually, even unused ones. The minibar tray is wiped, not just restocked.\n\nFinal inspection: +1 minute. The supervisor walks the room from the doorway, then sits on the bed and looks up. Different angles reveal different issues.\n\nThe 5-star difference is not better products or fancier equipment.\n\nIt is 11 minutes more attention.\n\nThat is what your guests pay for. And what they remember.",
     "#FacilityManagement #HotelOperations #Hospitality #Budapest #AparthotelManagement"),

    ("6", "20260514", "0700", "Supervisor 4-Week Training", "Team/Culture",
     "Clipboard and tablet on a desk with handwritten notes. Second pair of hands holding a pen, mid-discussion. Soft light. Optionally real training photo from CEEFM.",
     "A new CEEFM cleaning supervisor goes through a four-week structured program before they take over a property.\n\nWeek 1: Standards and protocols. They shadow a senior supervisor. They learn our SOPs by checking work, not by reading manuals. The first three days they say nothing. They watch. They write down questions. By Friday they are asking why we do something a specific way, and we expect them to push back if our reason is weak.\n\nWeek 2: Quality calibration. They run inspections under the senior supervisor's review. We compare scores on the same 30 rooms. If their assessment differs from the senior's by more than 5%, we walk through every disagreement until they align. This is the most important week.\n\nWeek 3: Team management. They take over scheduling and shift coordination on a single property. They run a difficult conversation with a team member, then debrief with their senior. They handle a guest or tenant complaint live.\n\nWeek 4: Solo supervision with daily check-ins. By the end of week 4, they should run the property without needing escalation for routine issues.\n\nWe do not promote based on tenure. We promote based on whether someone can run a quality check that consistently matches a senior's scoring.\n\nThat standard does not move.",
     "#FacilityManagement #PropertyOperations #Training #Budapest #FMCareers"),

    ("F2", "20260515", "1000", "+7% YoY Integrated FM Stat", "Amplification (Stat Graphic)",
     "Magazine-cover style stat card: massive +7% in Forest Green, subtitle 'Integrated FM contracts, CEE, year over year', subtle Sage Green trend line at bottom.",
     "Integrated facility management contracts in Central and Eastern Europe are growing 7% year over year.\n\nProperty owners stopped asking \"what is the cheapest cleaning contract?\"\n\nThey are asking: \"what is the full cost of running this building?\"\n\nDifferent question. Different answer.",
     "#FacilityManagement #IntegratedFM #CEERealEstate #Budapest"),

    ("7", "20260519", "0700", "Hospitality FM ≠ Residential FM", "Industry Insight",
     "Split-screen photo: hotel corridor with housekeeping cart on left, residential lobby with maintenance worker on right. Forest Green divider line.",
     "Treating a hotel like an apartment building is the most expensive mistake in facility management.\n\nThe differences run deeper than checklists.\n\nCycle. A hotel room turns over daily. A hospitality crew works to a 60-90 minute window between checkout and the next arrival. A residential building has weekly common-area cycles, monthly deep cleans, and seasonal capital work. The supervisor's calendar looks completely different.\n\nTolerance. A guest will write a 1-star review over a hair on a pillow. A tenant will tolerate the same hair for a week before mentioning it at the next building meeting. Same problem. Different expectation. Different staff training required.\n\nLiability. Hotel housekeeping carries acute risk: missed bedbug detection, sanitation failures, allergen exposure. Residential FM carries chronic risk: HVAC negligence, fire safety drift, mold accumulation. Acute risks need fast detection. Chronic risks need consistent monitoring.\n\nProcurement. Hotels buy disposables in volume on tight margins. Residential buildings buy durables that need to last 5-15 years. Different purchasing rhythm, different vendor relationships.\n\nReporting. Hotels report to operators who answer to brand standards. Residential FM reports to owners or boards who answer to investors or residents. Different metrics, different cadence.\n\nA team that can do both well is not running one playbook. They are running two.\n\nThis is why we built separate frameworks for hospitality and residential at CEEFM. More on what that looks like later this week.",
     "#FacilityManagement #HotelOperations #PropertyManagement #Hospitality #Budapest"),

    ("8", "20260520", "0700", "14-Category Aparthotel Standard Preview", "Industry Insight",
     "14 small category icons in a 7x2 or 4x4 grid (clipboard, towel, kitchen, fire extinguisher, energy meter etc.) on Warm Cream, Forest Green icons, Sage Green divider lines.",
     "The aparthotel category is growing fast in Budapest. Most operators run them like long-stay hotels. The good ones run them like nothing else.\n\nWe are publishing the CEEFM Aparthotel Operating Standard next month. 14 categories. Here is the list:\n\n1. Pre-arrival inspection cadence\n2. Mid-stay touchpoint policy (housekeeping vs guest privacy)\n3. Linen and towel rotation rules for stays of 3+ nights\n4. Kitchen-area cleaning (the failure point of most aparthotels)\n5. Common area maintenance during peak occupancy\n6. Maintenance escalation paths during off-hours\n7. Compliance documentation (fire, hygiene, accessibility)\n8. Energy management for variable occupancy\n9. Waste handling for self-catering units\n10. Pest control protocol for kitchens and storage\n11. Guest reporting and response time SLAs\n12. Vendor coordination for repairs that overlap occupancy\n13. Quality inspection schedule\n14. Pre-checkout protocol and turnover speed\n\nEach category has measurable thresholds. Each has a documented process. Each has accountability.\n\nThe framework is built from operations across our managed Budapest properties. It applies to single-unit conversions, full apartment-block aparthotels, and mixed-use buildings with serviced apartments.\n\nIf you operate aparthotels in Budapest and want a copy when it publishes, leave a comment or reach us at office@ceefm.eu.",
     "#FacilityManagement #AparthotelManagement #HotelOperations #Hospitality #Budapest"),

    ("9", "20260521", "0700", "Why Separate Hospitality and Residential Playbooks", "Company/Service",
     "Two-column visual: Hospitality icons (turnover clock, housekeeping cart, brand standard) vs Residential icons (calendar, common area, compliance binder), CEEFM logo as anchor.",
     "We could have written one facility management playbook and applied it everywhere.\n\nMost FM companies do.\n\nWe do not, because the cost of forcing one model on two industries shows up in three places:\n\nThe wrong staff in the wrong setting. A housekeeper trained for hotel turnovers in a 60-minute window cannot pace a residential common-area weekly clean. A residential maintenance technician cannot match the speed required for hotel room repairs between guests.\n\nThe wrong reporting. Hotel operators want occupancy-driven metrics: cost per occupied room, response time per ticket, brand audit scores. Residential boards want building-driven metrics: annual operating cost per square meter, compliance status, capital reserve trajectory. Same data points do not serve both.\n\nThe wrong vendors. Hotel-grade laundry, hotel-grade chemicals, hotel-grade procurement contracts do not translate to residential. The economics are wrong in both directions.\n\nWe run two separate playbooks at CEEFM. One for hospitality. One for residential. Each has its own quality framework, training program, supplier list, reporting cadence, and supervisor specialization.\n\nIf you operate in either category in Budapest, the right question is not \"do you do FM?\" It is \"do you do my type of FM?\"\n\nWe do. Both. Specifically.\n\nceefm.eu | office@ceefm.eu | +36 30 600 5400",
     "#FacilityManagement #HotelOperations #PropertyManagement #Budapest #IntegratedFM"),

    ("F3", "20260522", "1000", "Aparthotel Standard Snippet (Kitchen Cleaning)", "Amplification (Snippet)",
     "Bold typography card: '1 / 14' in Forest Green, 'Kitchen-area cleaning' subtitle, low-opacity grayscale aparthotel kitchen background, Sage Green accent line.",
     "1 of the 14 categories in our upcoming Aparthotel Operating Standard:\n\n**Kitchen-area cleaning.**\n\nThis is where most aparthotels fail. Not in the bedroom. Not in the bathroom.\n\nIn the kitchen.\n\nReason: housekeeping protocols designed for hotel rooms do not cover sinks where guests prepare actual meals. Grease accumulates faster than the cleaning frequency assumes. Guests notice within 24 hours. Reviews land within 48.\n\nThe fix is a separate kitchen protocol with its own checklist, frequency, and sign-off.\n\nWe will publish all 14 in June.",
     "#FacilityManagement #AparthotelManagement #Hospitality #Budapest"),

    ("10", "20260526", "0700", "120-Room Aparthotel Case Study", "Case/Proof (Anonymized)",
     "Three-stat card: -18% / -40% / 0 with labels 'Cost per room / Overtime / Supervisor turnover'. Forest Green numbers on Warm Cream. Aparthotel silhouette in Sage Green at bottom.",
     "A 120-room aparthotel in central Budapest came to us four months ago with three problems:\n\nHousekeeping costs were 28% above their budget.\nGuest reviews mentioned cleanliness in 11% of negative ratings.\nTheir previous FM provider had cycled three supervisors in eight months.\n\nWe did three things over 16 weeks:\n\nRestructured the housekeeping schedule around actual checkout patterns instead of fixed shift blocks. We reduced overtime by 40% just by mapping cleaning windows to when rooms were actually empty.\n\nReplaced 11 different cleaning products with 4 procurement-tier-rated alternatives. Same hygiene results. 22% lower per-room chemical cost. Less storage space needed.\n\nEmbedded a single supervisor on the property four days a week, with a clear scoring rubric we apply weekly. The team stopped guessing what good looked like.\n\nThe numbers four months in:\n\nHousekeeping cost per occupied room: down 18%\nCleanliness mentions in negative reviews: down to 3%\nSupervisor turnover: zero\n\nThis is the kind of result that comes from doing fewer things in more depth. Not from a bigger contract.\n\nIf you operate an aparthotel in Budapest and these numbers sound familiar, reach out: office@ceefm.eu",
     "#FacilityManagement #AparthotelManagement #HotelOperations #Hospitality #Budapest"),

    ("11", "20260527", "0700", "50-Unit Building - Visibility Fix", "Case/Proof (Anonymized)",
     "Before/after dashboard mockup: chaotic paper complaints on left vs clean digital ticket interface (Received/Scheduled/In progress/Resolved) on right. CEEFM colors.",
     "A 50-unit apartment building in District 13 came to us three months ago with one symptom: tenants were filing 60+ maintenance complaints per month.\n\nThe building manager assumed the problem was their maintenance team.\n\nIt was not.\n\nThe actual problem: there was no system for tracking which complaints had been resolved, which were duplicated, and which had been silently ignored. Tenants filed the same complaint three or four times because nothing visible happened the first time. The maintenance team was actually fixing things. They just had no way to communicate that.\n\nWhat we changed in 90 days:\n\nInstalled a digital ticketing system tenants could see. Every complaint got a status: received, scheduled, in progress, resolved. Average resolution time visible per ticket type.\n\nBuilt a weekly preventive walkthrough. The four most common complaint categories (lighting, hallway cleanliness, elevator noise, package handling) got a scheduled inspection before tenants reported them.\n\nReplaced the monthly building newsletter with a one-page operations summary: what got fixed, what is scheduled, what is pending, who to contact for what.\n\n90 days in:\n\nMaintenance complaints filed per month: down from 60+ to 12\nRepeat complaints (same issue, same tenant): down 80%\nTenant satisfaction survey: from 6.2 to 8.4 out of 10\n\nThe maintenance team did not change. The system around them did.\n\nMost building complaint problems are not work problems. They are visibility problems.",
     "#FacilityManagement #PropertyManagement #ResidentialFM #Budapest #BuildingManagement"),

    ("12", "20260528", "0700", "Q3 2026 Site Assessments Open", "Company/Service",
     "Clean CTA card: 'Q3 2026' in large Forest Green, '5 site assessments / No cost', email/phone/URL stacked. Sage Green divider line. Warm Cream background.",
     "We are opening Q3 2026 capacity for new property assessments.\n\nWho this is for:\n\nHotel and aparthotel operators in Budapest with 50+ keys looking for an integrated FM partner.\n\nResidential building owners or managers with 30+ units running multiple separate vendors and ready to consolidate.\n\nProperty funds or operators looking at portfolio-level FM standardization across Hungary.\n\nWhat a CEEFM site assessment covers:\n\nA walk-through of your property with a CEEFM senior supervisor. We look at the same 11 things we look at when we run our own quality checks. You see exactly what we see.\n\nA written report within 7 days. It identifies the 3 highest-impact gaps in your current operation, with cost-of-inaction estimates and the order we would address them.\n\nA scoping conversation. If we are a fit, we walk through what an engagement looks like for a property like yours. If we are not a fit, we tell you who is. Either way, the assessment is yours to keep.\n\nThere is no cost for the assessment.\n\nWe hold five Q3 slots and they fill in order. Reach out at office@ceefm.eu, +36 30 600 5400, or via the contact form at ceefm.eu/contact.",
     "#FacilityManagement #PropertyManagement #IntegratedFM #Budapest #PropertyOperations"),

    ("F4", "20260529", "1000", "Five FM Conversations This Month", "Amplification (Closing)",
     "Numbered list typography card with subtle quote-mark watermark. Forest Green numbers, Charcoal Gray text, Warm Cream background. CEEFM logo bottom corner.",
     "The five FM conversations we are having most often this month:\n\n1. \"We have grown beyond what our original cleaning company can do.\"\n2. \"Our vendor list is too long and the coordination is killing us.\"\n3. \"We are converting from long-stay to aparthotel and need an operating standard.\"\n4. \"Our energy bills doubled and we do not know which lever to pull first.\"\n5. \"Our maintenance complaints are not the work, they are the lack of visibility.\"\n\nIf any of these are familiar, our Q3 assessment slots are open. office@ceefm.eu",
     "#FacilityManagement #PropertyManagement #Budapest #IntegratedFM"),
]


def build_ics() -> str:
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//BridgeWorks//CEEFM Content Calendar//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:CEEFM May LinkedIn",
        "X-WR-TIMEZONE:Europe/Budapest",
    ]
    for num, date, hhmm, title, type_label, image, body, hashtags in EVENTS:
        end_hh = int(hhmm[:2])
        end_mm = int(hhmm[2:])
        end_total = end_hh * 60 + end_mm + 30
        end_hhmm = f"{end_total // 60:02d}{end_total % 60:02d}"
        summary = f"LinkedIn Post {num}: {title} [{type_label}]"
        desc = (
            f"TOPIC: {title}\n"
            f"TYPE: {type_label}\n\n"
            f"IMAGE BRIEF: {image}\n\n"
            f"--- ENGLISH ---\n{body}\n\n"
            f"{hashtags}"
        )
        lines += [
            "BEGIN:VEVENT",
            f"DTSTART:{date}T{hhmm}00Z",
            f"DTEND:{date}T{end_hhmm}00Z",
            f"SUMMARY:{ics_escape(summary)}",
            f"DESCRIPTION:{ics_escape(desc)}",
            "STATUS:CONFIRMED",
            f"UID:ceefm-may-post{num.lower()}@bridgeworks.agency",
            "END:VEVENT",
        ]
    lines.append("END:VCALENDAR")
    return "\r\n".join(lines) + "\r\n"


if __name__ == "__main__":
    OUT_PATH.write_text(build_ics(), encoding="utf-8")
    print(f"Wrote {len(EVENTS)} events to {OUT_PATH}")
