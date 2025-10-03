import streamlit as st
from UI.css import STYLE
from UI.html_snippet import HEADER, render_video_info, FOOTER
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
        st.markdown(STYLE, unsafe_allow_html=True)

    def reset(self):
        """Reseta o estado da sessão"""
        st.session_state.submitted = False
        st.session_state.video_url = ""
    
    def run(self):
        """Executa a interface principal"""
        st.markdown(HEADER, unsafe_allow_html=True)

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
                st.markdown(render_video_info(url, video_id, video_info), unsafe_allow_html=True)

            except Exception as e:
                st.warning(f"Could not load video thumbnail: {e}")
            
            st.success("Video analysis complete! (This is a placeholder message.)")
            
            if st.button("Analyze Another Video"):
                self.reset()
                st.rerun()
        
        #st.markdown(FOOTER, unsafe_allow_html=True)