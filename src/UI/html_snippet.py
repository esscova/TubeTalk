HEADER = """
            <div class="header-area">
                <h1>TubeTalk</h1>
                <h2>🤖 Your personal YouTube assistant</h2>
                <p>Analyze YouTube videos with ease!</p>
            </div>
            <p style='text-align: center; margin-top: 3rem;'>Developed by 
                <a href='https://www.linkedin.com/in/wellington-moreira-santos' target='_blank'>Wellington M Santos</a>
            </p>
        """
def render_video_info(url,video_id, video_info):
    return f"""
            <div>
                <h2 style='padding: 1rem;'>Here is the video you submitted:</h2>
                <iframe width='100%' height='315' src='https://www.youtube.com/embed/{video_id}' frameborder='0' style='margin-bottom: 1rem;'></iframe>
                <h2 class="video-section">Information about the video</h2>
                <div style='margin-top: 1rem;'>
                    <p><strong>URL:</strong> {url}</p>
                    <p><strong>Video ID:</strong> {video_id}</p>
                    <p><strong>Title:</strong> {video_info['title']}</p>
                    <p><strong>Author:</strong> {video_info['author']}</p>
                    <p><strong>Published on:</strong> {video_info['publish_date']}</p>
                    <p><strong>Views:</strong> {video_info['views']}</p>
                    <p><strong>Palavras-chave:</strong> {', '.join(video_info['keywords']) if video_info['keywords'] else 'N/A'}</p>
                </div>
                <hr style='margin: 2rem 0;' />                                    
                <h2 class="video-section">Summary</h2>
                <hr style='margin: 2rem 0;' />                                    
                <h2 class="video-section">Themes</h2>
                <hr style='margin: 2rem 0;' />                                    
            </div>
            """
FOOTER = """
            <div style='text-align: center; margin-top: 3rem; padding: 1rem; border-top: 1px solid #ccc;'>
                <h2>Thank you for using TubeTalk!</h2>
                <p>Developed by <a href='https://www.linkedin.com/in/wellington-moreira-santos' target='_blank'>Wellington M Santos</a></p>
            </div>
        """