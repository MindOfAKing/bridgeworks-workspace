import json, pathlib, datetime, urllib.request, xml.etree.ElementTree as ET, html, time
ROOT = pathlib.Path(r'C:/Users/User/Projects/bridgeworks-workspace')
watch = json.loads((ROOT/'youtube-watchlist.json').read_text(encoding='utf-8'))
now = datetime.datetime.now(datetime.timezone.utc)
published_after = now - datetime.timedelta(hours=18)
ns = {'atom':'http://www.w3.org/2005/Atom','yt':'http://www.youtube.com/xml/schemas/2015'}
results=[]; errors=[]
for cid in watch.get('follow',[]):
    url=f'https://www.youtube.com/feeds/videos.xml?channel_id={cid}'
    try:
        with urllib.request.urlopen(url, timeout=20) as r:
            xml=r.read()
        root=ET.fromstring(xml)
        for e in root.findall('atom:entry', ns):
            vid=(e.findtext('yt:videoId', default='', namespaces=ns) or '').strip()
            title=(e.findtext('atom:title', default='', namespaces=ns) or '').strip()
            author_el=e.find('atom:author/atom:name', ns)
            channel=author_el.text.strip() if author_el is not None and author_el.text else ''
            published=(e.findtext('atom:published', default='', namespaces=ns) or '').strip()
            try:
                dt=datetime.datetime.fromisoformat(published.replace('Z','+00:00'))
            except Exception:
                dt=None
            if vid and dt and dt >= published_after:
                media=e.find('{http://search.yahoo.com/mrss/}group')
                desc=''
                if media is not None:
                    d=media.find('{http://search.yahoo.com/mrss/}description')
                    desc=d.text.strip() if d is not None and d.text else ''
                results.append({'source':'rss-watchlist','channel_id':cid,'channel_label':watch.get('follow_labels',{}).get(cid,''),'video_id':vid,'title':html.unescape(title),'channel':channel,'publishedAt':published,'description':html.unescape(desc),'url':'https://www.youtube.com/watch?v='+vid})
        time.sleep(0.05)
    except Exception as ex:
        errors.append({'channel_id':cid,'error':type(ex).__name__})
seen=set(); ded=[]
for r in sorted(results, key=lambda x:x.get('publishedAt',''), reverse=True):
    if r['video_id'] not in seen:
        seen.add(r['video_id']); ded.append(r)
out = ROOT/'pipeline/youtube-scout'/f"latest-candidates-{now.date().isoformat()}-rss.json"
out.write_text(json.dumps({'published_after':published_after.isoformat(),'count':len(ded),'errors':errors,'items':ded}, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps({'source':'rss','published_after':published_after.isoformat(),'count':len(ded),'errors':len(errors),'file':str(out)}, indent=2))
for r in ded[:50]:
    print(f"{r['publishedAt']} | {r['channel']} | {r['title']} | {r['url']} | {r['channel_label']}")
