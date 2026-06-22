import sys, json, pathlib
from youtube_transcript_api import YouTubeTranscriptApi

def fetch(video_id):
    api = YouTubeTranscriptApi()
    # Try English first, then any transcript
    try:
        transcript = api.fetch(video_id, languages=['en','en-US','en-GB'])
    except Exception:
        transcript_list = api.list(video_id)
        transcript = None
        for t in transcript_list:
            transcript = t.fetch()
            break
        if transcript is None:
            raise
    lines=[]
    for s in transcript:
        start=getattr(s,'start', None) if not isinstance(s, dict) else s.get('start')
        text=getattr(s,'text', None) if not isinstance(s, dict) else s.get('text')
        if start is None or text is None: continue
        m=int(start//60); sec=int(start%60)
        lines.append(f"{m:02d}:{sec:02d} {text.replace(chr(10),' ')}")
    return '\n'.join(lines)

if __name__=='__main__':
    for vid in sys.argv[1:]:
        try:
            text=fetch(vid)
            out=pathlib.Path('pipeline/youtube-scout/runtime-transcripts')/(vid+'.txt')
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(text, encoding='utf-8')
            print(json.dumps({'video_id':vid,'chars':len(text),'file':str(out)}))
        except Exception as e:
            err=pathlib.Path('pipeline/youtube-scout/runtime-transcripts')/(vid+'.fetcherr')
            err.write_text(type(e).__name__+': '+str(e), encoding='utf-8')
            print(json.dumps({'video_id':vid,'error':type(e).__name__,'message':str(e)[:300]}))
