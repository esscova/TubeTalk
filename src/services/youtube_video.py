from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import yt_dlp
from datetime import datetime

def get_transcript(video_url: str) -> str | None:
    """Fetches and formats the transcript of a YouTube video given its URL."""
    try:
        video_id = video_url.split("v=")[1]
        languages = ["pt", "pt-BR", "en"]
        result = YouTubeTranscriptApi().fetch(video_id, languages=languages)
        formatter = TextFormatter()
        transcript_text = formatter.format_transcript(result)
        transcript_text = transcript_text.replace("\n", " ")
        return transcript_text
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None


def get_video_info(video_url: str) -> dict:
    ydl_opts = {'quiet': True, 'no_warnings': True, 'extract_flat': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        return {
            "title": info.get("title"),
            "author": info.get("uploader"),
            "publish_date": datetime.strptime(info.get("upload_date"), "%Y%m%d").date() if info.get("upload_date") else None,
            "views": info.get("view_count"),
            "length": info.get("duration"),
            "description": info.get("description"),
            "thumbnail_url": info.get("thumbnail"),
            "keywords": info.get("tags"),
            "rating": info.get("average_rating"),
        }

if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=Sm5jALppTLE"
    video_info = get_video_info(url)
    print(video_info)
    #print(get_transcript(url))
