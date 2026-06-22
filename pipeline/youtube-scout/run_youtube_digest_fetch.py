import json, os, urllib.parse, urllib.request, pathlib, datetime, time
ROOT = pathlib.Path(r'C:/Users/User/Projects/bridgeworks-workspace')
watch = json.loads((ROOT/'youtube-watchlist.json').read_text(encoding='utf-8'))
# Load env without printing secrets
env_path = pathlib.Path(r'C:/Users/User/Projects/.env')
if env_path.exists():
    for line in env_path.read_text(encoding='utf-8', errors='ignore').splitlines():
        if '=' in line and not line.strip().startswith('#'):
            k,v=line.split('=',1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
key = os.environ.get('YOUTUBE_API_KEY')
if not key:
    raise SystemExit('BLOCKER: YOUTUBE_API_KEY unavailable')
now = datetime.datetime.now(datetime.timezone.utc)
published_after = (now - datetime.timedelta(hours=14)).isoformat().replace('+00:00','Z')
base='https://www.googleapis.com/youtube/v3/search'
results=[]
def call(params):
    params = dict(params)
    params['key']=key
    url=base+'?'+urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=25) as r:
        return json.loads(r.read().decode('utf-8'))
# channels
for cid in watch.get('follow',[]):
    data=call({'part':'snippet','channelId':cid,'order':'date','type':'video','maxResults':3,'publishedAfter':published_after})
    for item in data.get('items',[]):
        vid=item.get('id',{}).get('videoId')
        sn=item.get('snippet',{})
        if vid:
            results.append({'source':'watchlist','channel_id':cid,'channel_label':watch.get('follow_labels',{}).get(cid,''),'video_id':vid,'title':sn.get('title',''),'channel':sn.get('channelTitle',''),'publishedAt':sn.get('publishedAt',''),'description':sn.get('description',''),'url':'https://www.youtube.com/watch?v='+vid})
    time.sleep(0.05)
# morning topic searches, bounded
for topic in watch.get('topics',[])[:12]:
    data=call({'part':'snippet','q':topic,'order':'date','type':'video','maxResults':3,'publishedAfter':published_after,'relevanceLanguage':'en'})
    for item in data.get('items',[]):
        vid=item.get('id',{}).get('videoId')
        sn=item.get('snippet',{})
        if vid:
            results.append({'source':'topic:'+topic,'channel_id':sn.get('channelId',''),'channel_label':'topic: '+topic,'video_id':vid,'title':sn.get('title',''),'channel':sn.get('channelTitle',''),'publishedAt':sn.get('publishedAt',''),'description':sn.get('description',''),'url':'https://www.youtube.com/watch?v='+vid})
    time.sleep(0.05)
# de-dupe sort newest
seen=set(); ded=[]
for r in sorted(results, key=lambda x:x.get('publishedAt',''), reverse=True):
    if r['video_id'] not in seen:
        seen.add(r['video_id']); ded.append(r)
out = ROOT/'pipeline/youtube-scout'/f"latest-candidates-{now.date().isoformat()}.json"
out.write_text(json.dumps(ded, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps({'published_after':published_after,'count':len(ded),'file':str(out)}, indent=2))
for r in ded[:40]:
    print(f"{r['publishedAt']} | {r['channel']} | {r['title']} | {r['url']} | {r['source']}")
