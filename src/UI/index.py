"""
    Interface de usuário principal para o aplicativo TubeTalk.
"""

import streamlit as st
from services import LLMService, YouTubeService
from configs.prompts import SUMMARY_PROMPT_TEMPLATE, TOPICS_PROMPT_TEMPLATE

class UI:
    def __init__(self):
        # 1. start do estado da sessão
        if "submitted" not in st.session_state:
            st.session_state.submitted = False
        if "video_url" not in st.session_state:
            st.session_state.video_url = ""
        if "video_data" not in st.session_state:
            st.session_state.video_data = None
        if "analysis_complete" not in st.session_state:
            st.session_state.analysis_complete = False
        if "analysis" not in st.session_state:
            st.session_state.analysis = None
        
        # 2. configs do LLM na sessao
        if "llm_provider" not in st.session_state:
            st.session_state.llm_provider = "openai"
        if "llm_model" not in st.session_state:
            st.session_state.llm_model = ""
        if "llm_api_key" not in st.session_state:
            st.session_state.llm_api_key = ""
        if "llm_temperature" not in st.session_state:
            st.session_state.llm_temperature = 0.7
        if "llm_max_tokens" not in st.session_state:
            st.session_state.llm_max_tokens = 1000

        # 3. estilos personalizados CSS
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
                    background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
                    padding: 0.5rem;
                    border-radius: 10px;
                    margin: 1rem 0;
                    text-align: center;
                    color: white;
                    font-weight: bold;
                }
                .info-card{
                    background: #f8f9fa;
                    padding: 1rem;
                    border-radius: 8px;
                    margin: 0.5rem 0;
                    border-left: 4px solid #fda085;
                }
                .summary-box{
                    background: white;
                    padding: 1.5rem;
                    border-radius: 10px;
                    border: 2px solid #f6d365;
                    margin: 1rem 0;
                    text-align: left;
                }
            </style>
        """, unsafe_allow_html=True)

    def reset(self):
        """Reseta o estado da sessão"""
        st.session_state.submitted = False
        st.session_state.video_url = ""
        st.session_state.video_data = None
        st.session_state.analysis_complete = False
        st.session_state.analysis = None
    
    def get_default_model(self, provider: str) -> str:
        """Retorna o modelo padrão para cada provedor"""
        defaults = {
            'openai': 'gpt-3.5-turbo',
            'ollama': 'llama2',
            'groq': 'mixtral-8x7b-32768',
            'huggingface': 'mistralai/Mistral-7B-Instruct-v0.1'
        }
        return defaults.get(provider, '')
    
    def render_settings(self):
        """Renderiza as configurações em um expander"""
        with st.expander("⚙️ Settings"):
            st.markdown("### 🤖 LLM Configuration")
            
            # provedor
            provider = st.selectbox(
                "LLM Provider",
                options=['openai', 'ollama', 'groq', 'huggingface'],
                format_func=lambda x: {
                    'openai': 'OpenAI (GPT)',
                    'ollama': 'Ollama (Local)',
                    'groq': 'Groq (Fast)',
                    'huggingface': 'HuggingFace'
                }[x],
                key='llm_provider'
            )
            
            # modelo
            default_model = self.get_default_model(provider)
            model = st.text_input(
                "Model Name",
                value=st.session_state.llm_model or default_model,
                placeholder=default_model,
                help=f"Default: {default_model}",
                key='llm_model'
            )
            
            if provider != 'ollama': # ollama nao precisa de chave
                api_key = st.text_input(
                    "API Key",
                    type="password",
                    value=st.session_state.llm_api_key,
                    placeholder="Deixe vazio para usar .env ",
                    help="Use sua chave de API do provedor selecionado",
                    key='llm_api_key'
                )
                
                # validar config do LLM
                validation = LLMService.validate_config(provider, api_key)
                if validation['valid']:
                    st.success("✅ Configuração válida!")
                else:
                    st.warning(f"⚠️ {validation['error']}")
            else:
                st.info("ℹ️ Ollama não requer chave de API, mas certifique-se de que o servidor local esteja em execução.")
            
            # parametros avançados
            st.markdown("### 🎛️ Parâmetros Avançados")

            temperature = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=1.0,
                value=st.session_state.llm_temperature,
                step=0.1,
                help="Valores mais altos resultam em respostas mais criativas",
                key='llm_temperature'
            )
            
            max_tokens = st.slider(
                "Max Tokens",
                min_value=100,
                max_value=2000,
                value=st.session_state.llm_max_tokens,
                step=100,
                help="Comprimento máximo do texto gerado",
                key='llm_max_tokens'
            )
            
            st.markdown("### 📋 Outras Configurações")
            st.checkbox("Auto-play videos", value=False)
            st.checkbox("Show full transcript", value=False)
    
    def extract_transcript(self, url: str):
        """Extrai a transcrição do vídeo"""
        with st.spinner("🎬 Extraindo transcrição..."):
            service = YouTubeService()
            video_data = service.get_complete_data(url)
            
            if not video_data['success']:
                st.error(f"❌ {video_data['error']}")
                return None
            
            st.session_state.video_data = video_data
            return video_data
    
    def analyze_with_llm(self, transcript: str):
        """Analisa a transcrição com o LLM configurado"""
        try:
            # 1. startar LLM com as configs
            with st.spinner(f"🤖 Gerando com: {st.session_state.llm_provider.upper()}..."):
                llm_service = LLMService(
                    provider=st.session_state.llm_provider,
                    model_name=st.session_state.llm_model or None,
                    api_key=st.session_state.llm_api_key or None,
                    temperature=st.session_state.llm_temperature,
                    max_tokens=st.session_state.llm_max_tokens
                )
                
                # 2. gerar resumo
                summary_result = llm_service.generate_summary(
                    transcript=transcript,
                    prompt_template=SUMMARY_PROMPT_TEMPLATE
                )
                
                if not summary_result['success']:
                    st.error(f"❌ Summary generation failed: {summary_result['error']}")
                    return None
                
                # 3. topicos principais
                topics_result = llm_service.extract_topics(
                    transcript=transcript,
                    prompt_template=TOPICS_PROMPT_TEMPLATE
                )
                
                if not topics_result['success']:
                    st.error(f"❌ Topics extraction failed: {topics_result['error']}")
                    return None
                
                return {
                    'summary': summary_result['summary'],
                    'topics': topics_result['topics']
                }
                
        except Exception as e:
            st.error(f"❌ Falha ao analisar: {str(e)}")
            st.info("💡 **Dicas de solução de problemas:**\n"
                   "- Verifique sua chave de API nas Configurações\n"
                   "- Verifique sua conexão com a internet\n"
                   "- Tente um modelo ou provedor diferente\n"
                   "- Se estiver usando Ollama, verifique se está em execução localmente")
            return None
    
    def render_video_analysis(self, video_data: dict, analysis: dict):
        """Renderiza a seção de análise do vídeo"""
        video_id = video_data['video_id']
        
        st.markdown(f"""
            <div style='text-align: center;'>
                <h2 style='padding: 1rem;'>📺 Video Analysis</h2>
                <iframe width='100%' height='315' src='https://www.youtube.com/embed/{video_id}' frameborder='0' allowfullscreen style='margin-bottom: 1rem; border-radius: 10px;'></iframe>
            </div>
        """, unsafe_allow_html=True)
        
        # 1. cards com infos do vídeo
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
                <div class='info-card'>
                    <strong>🆔 Video ID:</strong><br>
                    <code>{video_id}</code>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class='info-card'>
                    <strong>🌐 Language:</strong><br>
                    {video_data['transcript_language'].upper()}
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
                <div class='info-card'>
                    <strong>📝 Segments:</strong><br>
                    {video_data['duration']}
                </div>
            """, unsafe_allow_html=True)
        
        # 2. resumo
        st.markdown("<h2 class='video-section'>📄 Summary</h2>", unsafe_allow_html=True)
        st.markdown(f"""
            <div class='summary-box'>
                {analysis['summary'].replace(chr(10), '<br>')}
            </div>
        """, unsafe_allow_html=True)
        
        # 2. tpicos
        st.markdown("<h2 class='video-section'>🎯 Main Topics</h2>", unsafe_allow_html=True)
        st.markdown(f"""
            <div class='summary-box'>
                {analysis['topics'].replace(chr(10), '<br>')}
            </div>
        """, unsafe_allow_html=True)
    
    def run(self):
        """Executa a interface principal"""
        # 1. render header
        st.markdown("""
            <div class="header-area">
                <h1>TubeTalk</h1>
                <h2>🤖 Your personal YouTube assistant</h2>
                <p>Analyze YouTube videos with AI-powered insights!</p>
            </div>
        """, unsafe_allow_html=True)
        
        # 2. configs
        self.render_settings()
        
        # main
        if not st.session_state.submitted:
            # Tela de input
            st.markdown("<p style='font-size: 1.5rem; font-weight: bold; text-align: center;'>Insira uma URL de vídeo do YouTube para começar:</p>", unsafe_allow_html=True)
            st.text_input(
                "",
                key="video_url",
                placeholder="https://www.youtube.com/watch?v=example",
                label_visibility="collapsed",
                max_chars=200,
                help="Insira uma URL de vídeo do YouTube válida."
            )

            if st.button("🔍 Analisar Vídeo", use_container_width=True):
                url = st.session_state.video_url.strip()
                if url: # url?
                    video_data = self.extract_transcript(url)
                   
                    if video_data: #dados?
                        analysis = self.analyze_with_llm(video_data['transcript'])
                        
                        if analysis: # analise?
                            st.session_state.video_data = video_data
                            st.session_state.analysis = analysis
                            st.session_state.submitted = True
                            st.session_state.analysis_complete = True
                            st.rerun()
                else:
                    st.error("❌ Please enter a valid YouTube video URL.")
            
            st.markdown("<p style='text-align: center; margin-top: 3rem;'>Developed by <a href='https://www.linkedin.com/in/wellington-moreira-santos' target='_blank'>Wellington M Santos</a></p>", unsafe_allow_html=True)
        
        else:
            # tela geral de analise
            if st.session_state.analysis_complete and st.session_state.video_data: # dados e analise?
                self.render_video_analysis(
                    st.session_state.video_data,
                    st.session_state.analysis
                )
                
                # reset
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🔄 Analisar Outro Vídeo", use_container_width=True):
                    self.reset()
                    st.rerun()
            else:
                st.error("❌ Análise não disponível. Por favor, tente novamente.")
                if st.button("← Voltar para a Página Inicial"):
                    self.reset()
                    st.rerun()