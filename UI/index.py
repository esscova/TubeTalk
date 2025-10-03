import streamlit as st
from services.youtube_video import get_video_info

class UI:
    def __init__(self):
        # Inicialização do estado da sessão
        if "submitted" not in st.session_state:
            st.session_state.submitted = False
        if "video_url" not in st.session_state:
            st.session_state.video_url = ""

        # Configuração da página
        st.set_page_config(page_title="TubeTalk", page_icon="💡", layout="centered")

        # Estilos personalizados
        st.markdown("""
            <style>
                .header-area{
                    text-align: center;
                    margin-bottom: 2rem;
                    padding: 1rem;
                    border-radius: 10px;
                    background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
                }
                .video-section{
                    text-align: center;
                    background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
                    padding: 0.5rem;
                    border-radius: 10px;
                    margin: 2rem 0;
                }
            </style>
        """, unsafe_allow_html=True)

    def reset(self):
        """Reseta o estado da sessão"""
        st.session_state.submitted = False
        st.session_state.video_url = ""
    
    def run(self):
        """Executa a interface principal"""
        st.markdown("""
                        <div class="header-area">
                            <h1>TubeTalk</h1>
                            <h2>🤖 Your personal YouTube assistant</h2>
                            <p>Analyze YouTube videos with ease!</p>
                        </div>
                        <p style='text-align: center; margin-top: 3rem;'>Developed by 
                            <a href='https://www.linkedin.com/in/wellington-moreira-santos' target='_blank'>Wellington M Santos</a>
                        </p>
                    """, unsafe_allow_html=True)

        if not st.session_state.submitted:
            st.markdown("<p style='font-size: 1.5rem; font-weight: bold; text-align: center; '>Enter a YouTube video URL to get started:</p>", unsafe_allow_html=True)
            st.text_input("",
                          key="video_url",
                          icon="🔗",
                          placeholder="https://www.youtube.com/watch?v=example",
                          label_visibility="collapsed", 
                          max_chars=100, 
                          help="Enter a valid YouTube video URL.")

            if st.button("Analyze Video"):
                url = st.session_state.video_url.strip()
                if url:
                    st.session_state.submitted = True
                    st.rerun()
                else:
                    st.error("Please enter a valid YouTube video URL.")
            #st.markdown("<p style='text-align: center; margin-top: 3rem;'>Developed by <a href='https://www.linkedin.com/in/wellington-moreira-santos' target='_blank'>Wellington M Santos</a></p>", unsafe_allow_html=True)
        else:
            url = st.session_state.video_url
            try:
                if "youtu.be/" in url:
                    video_id = url.split("youtu.be/")[1].split("?")[0].split("&")[0]
                elif "v=" in url:
                    video_id = url.split("v=")[1].split("&")[0].split("?")[0]
                else:
                    raise ValueError("Invalid URL format")
                
                video_info = get_video_info(url)
                st.markdown(f"""
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
                            """, unsafe_allow_html=True)


            except Exception as e:
                st.warning(f"Could not load video thumbnail: {e}")
            
            st.success("Video analysis complete! (This is a placeholder message.)")
            
            if st.button("Analyze Another Video"):
                self.reset()
                st.rerun()