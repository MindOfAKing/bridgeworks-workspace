import sys
import json
from youtube_transcript_api import YouTubeTranscriptApi


def fetch_transcript(video_url):
    video_id = video_url.split('v=')[-1] if 'v=' in video_url else video_url.split('/')[-1]
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    url = sys.argv[1]
    transcript = fetch_transcript(url)
    print(json.dumps(transcript))
