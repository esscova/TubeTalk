import streamlit as st

class UI:
    def __init__(self):
        # Inicialização do estado da sessão
        if "submitted" not in st.session_state:
            st.session_state.submitted = False
        if "video_url" not in st.session_state:
            st.session_state.video_url = ""
    
    def reset(self):
        """Reseta o estado da sessão"""
        st.session_state.submitted = False
        st.session_state.video_url = ""
    
    def run(self):
        """Executa a interface principal"""
        # --- Conteúdo da página ---
        st.title("TubeTalk")
        st.subheader("Your personal YouTube assistant")
        
        if not st.session_state.submitted:
            st.text_input("Enter your YouTube video URL:", key="video_url")
            if st.button("Analyze Video"):
                url = st.session_state.video_url.strip()
                if url:
                    st.session_state.submitted = True
                    st.rerun()
                else:
                    st.error("Please enter a valid YouTube video URL.")
        else:
            url = st.session_state.video_url
            st.write(f"Analyzing video: {url}")
            
            try:
                if "youtu.be/" in url:
                    video_id = url.split("youtu.be/")[1].split("?")[0].split("&")[0]
                elif "v=" in url:
                    video_id = url.split("v=")[1].split("&")[0].split("?")[0]
                else:
                    raise ValueError("Invalid URL format")
                
                st.markdown(
                    f"<iframe width='560' height='315' src='https://www.youtube.com/embed/{video_id}' frameborder='0'></iframe>",
                    unsafe_allow_html=True
                )
            except Exception as e:
                st.warning(f"Could not load video thumbnail: {e}")
            
            st.success("Video analysis complete! (This is a placeholder message.)")
            
            if st.button("Analyze Another Video"):
                self.reset()
                st.rerun()