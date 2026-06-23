
import os, json, base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

drafts = [{"key": "managerent", "to": "info@managerent.hu", "subject": "Small trust leak on your English property management page", "body": "Hi Managerent team,\n\nI was reviewing Budapest property management firms that serve overseas owners and noticed something small that may be costing enquiries.\n\nYour offer is strong. You clearly understand the foreign-owner problem: tenant screening, rent collection, maintenance, accounting, legal support, and online visibility.\n\nThe issue is that a few English copy errors on the management page may weaken trust before an overseas investor contacts you. For example, words like “frist”, “exterenal”, “begining”, and “acces” stand out because your ideal client is choosing someone to manage a valuable asset from abroad.\n\nI do not think this needs a full rebuild. It looks more like a trust and enquiry-flow cleanup.\n\nIf useful, I can send over 3 quick observations from a 48-hour Lead Leak Review.\n\nBest,\nEmmanuel Ehigbai\nBridgeWorks\noffice@bridgeworks.agency"}, {"key": "craftex", "to": "info@craftex.hu", "subject": "Quick note on Craftex’s quote path", "body": "Hi Craftex team,\n\nI was reviewing Budapest construction, renovation, and maintenance firms and noticed something that may be worth fixing.\n\nYour site does a good job explaining the process: consultation, site visit, quote, design, planning, execution, and handover. That gives clients a clear sense of order.\n\nThe possible leak is around trust and quote conversion. If the counters like “Team Members 0+”, “Projects Completed 0+”, or “Languages 0+” are visible on the live site, they may weaken confidence at the exact point where a client is deciding whether to request a quote.\n\nI also think your commercial services could be easier to separate from residential work, especially for offices, clinics, hospitality, and property investors.\n\nIf useful, I can send over 3 quick observations from a 48-hour Lead Leak Review.\n\nBest,\nEmmanuel Ehigbai\nBridgeWorks\noffice@bridgeworks.agency"}, {"key": "aplus-real-estate", "to": "info@aplusproperty.hu", "subject": "Small trust issue on high-value property listings", "body": "Hi A+ Real Estate team,\n\nI was reviewing Budapest property firms and noticed something small that may matter because your listings are high value.\n\nYour site shows strong investment appeal. Some listed properties are above 200M HUF, and the service mix of buying, selling, renting, property management, renovation, and investment support is valuable.\n\nThe possible leak is that premium listings need premium trust signals. A few visible copy issues, such as listing-title typos like “FOR SELE” and “TOW BALCONIES”, may reduce confidence before a buyer or investor submits an enquiry.\n\nI do not think this means the site is broken. It looks like a trust and enquiry-flow cleanup opportunity.\n\nIf useful, I can send over 3 quick observations from a 48-hour Lead Leak Review.\n\nBest,\nEmmanuel Ehigbai\nBridgeWorks\noffice@bridgeworks.agency"}]
home = os.path.expanduser('~')
token_path = os.path.join(home, 'AppData', 'Local', 'hermes', 'google_token.json')
creds = Credentials.from_authorized_user_file(token_path)
service = build('gmail', 'v1', credentials=creds)
results=[]
for d in drafts:
    msg = MIMEText(d['body'], 'plain', 'utf-8')
    msg['To'] = d['to']
    msg['Subject'] = d['subject']
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode('utf-8')
    draft = service.users().drafts().create(userId='me', body={'message': {'raw': raw}}).execute()
    results.append({'key': d['key'], 'to': d['to'], 'subject': d['subject'], 'draft_id': draft.get('id'), 'message_id': draft.get('message', {}).get('id')})
print(json.dumps(results, indent=2))
