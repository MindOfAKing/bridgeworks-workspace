
import csv, json, re
from pathlib import Path
from datetime import datetime, date

ROOT = Path(__file__).resolve().parents[1]
DASH = Path(__file__).resolve().parent
TRACKER = ROOT / '01-prospects' / 'prospect-tracker.csv'
SEND_LOG = ROOT / '03-outreach-drafts' / 'outreach-send-log-2026-06-23.json'
BATCH2_SUMMARY = ROOT / '02-lead-leak-reviews' / 'batch-2' / 'batch-2-summary.md'
NEXT_STEPS = ROOT / '05-os-build-next' / 'bridgeworks-os-next-steps-2026-06-23.md'

def read_text(path):
    try:
        return path.read_text(encoding='utf-8')
    except FileNotFoundError:
        return ''

def parse_date(s):
    if not s:
        return None
    try:
        return date.fromisoformat(s)
    except Exception:
        return None

rows=[]
if TRACKER.exists():
    with TRACKER.open(newline='', encoding='utf-8') as f:
        rows=list(csv.DictReader(f))

today=date.today()
counts={}
score_counts={}
for r in rows:
    counts[r.get('status','(blank)') or '(blank)']=counts.get(r.get('status','(blank)') or '(blank)',0)+1
    score_counts[r.get('lead_score_hot_warm_cold','(blank)') or '(blank)']=score_counts.get(r.get('lead_score_hot_warm_cold','(blank)') or '(blank)',0)+1

sent=[r for r in rows if 'Sent' in (r.get('status') or '')]
waiting=[r for r in rows if 'waiting' in (r.get('status') or '').lower()]
batch2=[r for r in rows if 'Batch 2' in (r.get('status') or '')]
reviews=[r for r in rows if 'Reviewed' in (r.get('status') or '')]
upcoming=[]
overdue=[]
for r in rows:
    d=parse_date(r.get('next_follow_up',''))
    if d:
        item={'business':r['business_name'],'date':d.isoformat(),'status':r.get('status',''),'days':(d-today).days}
        if d < today: overdue.append(item)
        else: upcoming.append(item)
upcoming=sorted(upcoming, key=lambda x:x['date'])

def extract_md_bullets(text, max_lines=8):
    out=[]
    for line in text.splitlines():
        if line.startswith('- ') or re.match(r'^\d+\. ', line):
            out.append(line)
        if len(out)>=max_lines: break
    return out

data={
    'generated_at': datetime.now().isoformat(timespec='seconds'),
    'root': str(ROOT),
    'summary': {
        'total_prospects': len(rows),
        'sent_waiting': len(waiting),
        'batch2_prepared': len(batch2),
        'reviewed_not_sent': len(reviews),
        'next_follow_up': upcoming[0] if upcoming else None,
        'overdue_count': len(overdue),
    },
    'counts_by_status': counts,
    'counts_by_score': score_counts,
    'prospects': rows,
    'upcoming_followups': upcoming,
    'overdue_followups': overdue,
    'send_log': json.loads(read_text(SEND_LOG) or '{}'),
    'batch2_summary_lines': extract_md_bullets(read_text(BATCH2_SUMMARY), 12),
    'next_steps_lines': extract_md_bullets(read_text(NEXT_STEPS), 16),
    'files': {
        'tracker': str(TRACKER),
        'send_log': str(SEND_LOG),
        'batch2_summary': str(BATCH2_SUMMARY),
        'next_steps': str(NEXT_STEPS),
    }
}
(DASH/'dashboard-data.json').write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps({'status':'ok','prospects':len(rows),'output':str(DASH/'dashboard-data.json')}, indent=2))
