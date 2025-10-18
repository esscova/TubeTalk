"""
Serviço para extração de transcrições e informações de vídeos do YouTube
"""

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import yt_dlp
from datetime import datetime
from typing import Optional, Dict


class YouTubeService:
    """Serviço para interagir com vídeos do YouTube"""
    
    def __init__(self, languages: list = None):
        """
        Inicializa o serviço
        
        Args:
            languages: Lista de idiomas preferidos para transcrições
        """
        self.languages = languages or ["pt", "pt-BR", "en", "en-US"]
    
    @staticmethod
    def extract_video_id(url: str) -> Optional[str]:
        """
        Extrai o ID do vídeo de uma URL do YouTube
        
        Args:
            url: URL do vídeo do YouTube
            
        Returns:
            video_id ou None se inválido
        """
        try:
            if "youtu.be/" in url:
                video_id = url.split("youtu.be/")[1].split("?")[0].split("&")[0]
            elif "v=" in url:
                video_id = url.split("v=")[1].split("&")[0].split("?")[0]
            else:
                return None
            
            if len(video_id) == 11: # id tem 11 carcteres?
                return video_id
            return None
            
        except Exception:
            return None
    
    def get_transcript(self, video_url: str) -> Dict[str, any]:
        """
        Obtém a transcrição de um vídeo do YouTube
        
        Args:
            video_url: URL do vídeo do YouTube
            
        Returns:
            Dict com 'success', 'transcript', 'language' e 'error'
        """
        try:
            # video_id = video_url.split("v=")[1]
            video_id = self.extract_video_id(video_url)            
            result = YouTubeTranscriptApi().fetch(video_id, languages=self.languages)
            formatter = TextFormatter()
            transcript_text = formatter.format_transcript(result)
            transcript_text = transcript_text.replace("\n", " ")
            
            return {
                'success': True,
                'transcript': transcript_text,
                'language': self.languages[0],
                'is_generated': True,
                'error': None
            }
            
        except Exception as e:
            return {
                'success': False,
                'transcript': None,
                'language': None,
                'error': f'Error fetching transcript: {str(e)}'
            }
    
    def get_video_info(self, video_url: str) -> Dict[str, any]:
        """
        Obtém informações detalhadas do vídeo usando yt-dlp
        
        Args:
            video_url: URL do vídeo do YouTube
            
        Returns:
            Dict com informações do vídeo
        """
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False  
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)                
                publish_date = None
                if info.get("upload_date"):
                    try:
                        publish_date = datetime.strptime(info.get("upload_date"), "%Y%m%d").date()
                    except:
                        publish_date = None
                
                return {
                    'success': True,
                    'video_id': info.get("id"),
                    'title': info.get("title"),
                    'author': info.get("uploader"),
                    'channel': info.get("channel"),
                    'publish_date': publish_date,
                    'views': info.get("view_count"),
                    'likes': info.get("like_count"),
                    'duration': info.get("duration"),  # em segundos
                    'description': info.get("description"),
                    'thumbnail_url': info.get("thumbnail"),
                    'keywords': info.get("tags", []),
                    'rating': info.get("average_rating"),
                    'category': info.get("categories", [None])[0] if info.get("categories") else None,
                    'error': None
                }
                
        except Exception as e:
            return {
                'success': False,
                'video_id': None,
                'error': f'Error fetching video info: {str(e)}'
            }
    
    def get_complete_data(self, video_url: str) -> Dict[str, any]:
        """
        Obtém tanto a transcrição quanto as informações do vídeo
        
        Args:
            video_url: URL do vídeo do YouTube
            
        Returns:
            Dict com transcrição e informações do vídeo combinadas
        """
        # 1. obtem informações do vídeo
        video_info = self.get_video_info(video_url)
        
        if not video_info['success']:
            return video_info
        
        # 2. busca transcrição
        transcript_data = self.get_transcript(video_url)
        
        # 3. dados
        return {
            'success': transcript_data['success'],
            'video_id': video_info['video_id'],
            'title': video_info['title'],
            'author': video_info['author'],
            'channel': video_info['channel'],
            'publish_date': video_info['publish_date'],
            'views': video_info['views'],
            'likes': video_info['likes'],
            'duration': video_info['duration'],
            'description': video_info['description'],
            'thumbnail_url': video_info['thumbnail_url'],
            'keywords': video_info['keywords'],
            'category': video_info['category'],
            'transcript': transcript_data.get('transcript'),
            'transcript_language': transcript_data.get('language'),
            'transcript_is_generated': transcript_data.get('is_generated'),
            'error': transcript_data.get('error')
        }
    
    @staticmethod
    def format_duration(seconds: int) -> str:
        """
        Formata duração de segundos para HH:MM:SS
        
        Args:
            seconds: Duração em segundos
            
        Returns:
            String formatada (ex: "10:30" ou "1:05:45")
        """
        if not seconds:
            return "N/A"
        
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes}:{secs:02d}"
    
    @staticmethod
    def format_views(views: int) -> str:
        """
        Formata número de visualizações
        
        Args:
            views: Número de visualizações
            
        Returns:
            String formatada (ex: "1.2M", "450K", "1.5K")
        """
        if not views:
            return "N/A"
        
        if views >= 1_000_000:
            return f"{views / 1_000_000:.1f}M"
        elif views >= 1_000:
            return f"{views / 1_000:.1f}K"
        else:
            return str(views)


if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=Sm5jALppTLE"
    service = YouTubeService()
    
    print("=== COMPLETE DATA ===")
    data = service.get_complete_data(url)
    
    if data['success']:
        print(f"Title: {data['title']}")
        print(f"Author: {data['author']}")
        print(f"Duration: {YouTubeService.format_duration(data['duration'])}")
        print(f"Views: {YouTubeService.format_views(data['views'])}")
        print(f"Transcript Language: {data['transcript_language']}")
        print(f"Transcript: {data['transcript'][:200]}...")
    else:
        print(f"Error: {data['error']}")