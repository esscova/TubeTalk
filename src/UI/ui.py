"""
    Interface de usuário principal para o aplicativo TubeTalk.
"""

import streamlit as st
from services import LLMService, YouTubeService
from configs.prompts import SUMMARY_PROMPT_TEMPLATE, TOPICS_PROMPT_TEMPLATE, ARTICLE_PROMPT_TEMPLATE

"""
Interface de usuário principal para o aplicativo TubeTalk.
"""

import streamlit as st
from services import LLMService, YouTubeService
from configs.prompts import SUMMARY_PROMPT_TEMPLATE, TOPICS_PROMPT_TEMPLATE, ARTICLE_PROMPT_TEMPLATE


class UI:
    def __init__(self):
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
        st.session_state.submitted = False
        st.session_state.video_url = ""
        st.session_state.video_data = None
        st.session_state.analysis_complete = False
        st.session_state.analysis = None

    def get_default_model(self, provider: str) -> str:
        defaults = {
            'openai': 'gpt-3.5-turbo',
            'ollama': 'llama2',
            'groq': 'llama-3.3-70b-versatile',
            'huggingface': 'mistralai/Mistral-7B-Instruct-v0.1'
        }
        return defaults.get(provider, '')

    def render_settings(self):
        with st.sidebar:
            st.markdown("### ⚙️ LLM Configuration")

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

            default_model = self.get_default_model(provider)
            st.text_input(
                "Model Name",
                value=st.session_state.llm_model or default_model,
                placeholder=default_model,
                help=f"Default: {default_model}",
                key='llm_model'
            )

            if provider != 'ollama':
                st.text_input(
                    "API Key",
                    type="password",
                    value=st.session_state.llm_api_key,
                    placeholder="Deixe vazio para usar .env",
                    help="Use sua chave de API do provedor selecionado",
                    key='llm_api_key'
                )

                validation = LLMService.validate_config(provider, st.session_state.llm_api_key)
                if validation['valid']:
                    st.success("✅ Configuração válida!")
                else:
                    st.warning(f"⚠️ {validation['error']}")
            else:
                st.info("ℹ️ Ollama não requer chave de API (local).")

            st.markdown("---")
            st.markdown("### 🎛️ Parâmetros Avançados")
            st.slider("Temperature", min_value=0.0, max_value=1.0, value=st.session_state.llm_temperature, step=0.1, key='llm_temperature')
            st.slider("Max Tokens", min_value=100, max_value=1000, value=st.session_state.llm_max_tokens, step=100, key='llm_max_tokens')

            st.markdown("---")
            st.info("💡 Teste sua configuração de LLM antes de analisar vídeos.")
            st.button("Test LLM", on_click=self._test_llm)

    def _test_llm(self):
        try:
            llm = LLMService(provider=st.session_state.llm_provider, model_name=st.session_state.llm_model or None, api_key=st.session_state.llm_api_key or None)
            res = llm.generate("Diga 'ok'")

            text = res.get('text') if res else None
            error = res.get('error') if res else 'Unknown error'
            verbose = False
            if error:
                verbose = len(str(error)) > 60
            else:
                verbose = text is None or len(str(text)) > 40

            msg = ''
            if res and res.get('success'):
                msg = f"LLM respondeu: {text}" if text else "LLM respondeu com sucesso"
            else:
                msg = f"Erro ao contatar LLM: {error}"
            if verbose:
                with st.sidebar:
                    if res and res.get('success'):
                        st.success(msg)
                    else:
                        st.error(msg)
            else:
                if res and res.get('success'):
                    st.success(msg)
                else:
                    st.error(msg)
        except Exception as e:
            with st.sidebar:
                st.error(f"Falha ao testar LLM: {e}")

    def extract_transcript(self, url: str):
        with st.spinner("🎬 Extraindo transcrição..."):
            service = YouTubeService()
            video_data = service.get_complete_data(url)

            if not video_data['success']:
                st.error(f"❌ {video_data['error']}")
                return None

            st.session_state.video_data = video_data
            return video_data

    def analyze_with_llm(self, transcript: str, video_data: dict = None):
        try:
            with st.spinner(f"🤖 Gerando com: {st.session_state.llm_provider.upper()}..."):
                llm_service = LLMService(
                    provider=st.session_state.llm_provider,
                    model_name=st.session_state.llm_model or None,
                    api_key=st.session_state.llm_api_key or None,
                    temperature=st.session_state.llm_temperature,
                    max_tokens=st.session_state.llm_max_tokens
                )

                summary_result = llm_service.generate_summary(
                    transcript=transcript,
                    prompt_template=SUMMARY_PROMPT_TEMPLATE
                )

                if not summary_result['success']:
                    st.error(f"❌ Summary generation failed: {summary_result['error']}")
                    return None

                topics_result = llm_service.extract_topics(
                    transcript=transcript,
                    prompt_template=TOPICS_PROMPT_TEMPLATE
                )

                if not topics_result['success']:
                    st.error(f"❌ Topics extraction failed: {topics_result['error']}")
                    return None

                article_result = llm_service.generate_article(
                    transcript=transcript,
                    prompt_template=ARTICLE_PROMPT_TEMPLATE,
                    length='long'
                )
                if not article_result['success']:
                    st.error(f"❌ Article generation failed: {article_result['error']}")
                    return None

                return {
                    'summary': summary_result['summary'],
                    'topics': topics_result['topics'],
                    'article': article_result['article']
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
        video_id = video_data['video_id']

        st.markdown(f"""
            <div style='text-align: center;'>
                <h2 style='padding: 1rem;'>📺 Video Analysis</h2>
                <iframe width='100%' height='315' src='https://www.youtube.com/embed/{video_id}' frameborder='0' allowfullscreen style='margin-bottom: 1rem; border-radius: 10px;'></iframe>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<h2 class='video-section'>Metadados do Vídeo</h2>", unsafe_allow_html=True)
        st.write(f"**{video_data['title']}**")
        st.write(f"Author: {video_data['author']}")
        st.write(f"Canal: {video_data['channel']}")
        st.write(f"Published on: {video_data['publish_date']}")
        st.write(f"views: {video_data['views']} | likes: {video_data.get('like_count', 'N/A')} ")
        st.write(f"Palavras chave: {video_data.get('keywords', 'N/A')}")

        st.markdown("<h2 class='video-section'>📄 Resumo</h2>", unsafe_allow_html=True)
        st.markdown(f"""
            <div class='summary-box'>
                {analysis['summary'].replace(chr(10), '<br>')}
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<h2 class='video-section'>🎯 Tópicos Principais</h2>", unsafe_allow_html=True)
        st.markdown(analysis['topics'])

        st.markdown("<h2 class='video-section'>📰 Artigo Gerado</h2>", unsafe_allow_html=True)
        st.markdown(analysis['article'])

    def run(self):
        st.markdown("""
            <div class="header-area">
                <h1>TubeTalk</h1>
                <h2>🤖 Your personal YouTube assistant</h2>
                <p>Analyze YouTube videos with AI-powered insights!</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<p style='text-align: center; margin-top: 0.5rem;'>Developed by <a href='https://www.linkedin.com/in/wellington-moreira-santos' target='_blank'>Wellington M Santos</a></p>", unsafe_allow_html=True)

        st.markdown("---")

        self.render_settings()

        if not st.session_state.submitted:
            st.markdown("<p style='font-size: 1.5rem; font-weight: bold; text-align: center;'>Insira uma URL de vídeo do YouTube para começar:</p>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 3, 1])
            with col2:
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
                    if url:
                        video_data = self.extract_transcript(url)

                        if video_data:
                            analysis = self.analyze_with_llm(video_data['transcript'], video_data)

                            if analysis:
                                st.session_state.video_data = video_data
                                st.session_state.analysis = analysis
                                st.session_state.submitted = True
                                st.session_state.analysis_complete = True
                                st.rerun()
                    else:
                        st.error("❌ Please enter a valid YouTube video URL.")
        else:
            if st.session_state.analysis_complete and st.session_state.video_data:
                video_data = st.session_state.video_data
                analysis = st.session_state.analysis

                st.markdown(f"### {video_data.get('title', '')}")
                col_thumb, col_meta = st.columns([2, 1])
                with col_thumb:
                    if video_data.get('thumbnail_url'):
                        st.image(video_data['thumbnail_url'], use_container_width=False, width='content')
                with col_meta:
                    st.write(f"**Canal:** {video_data.get('channel', '')}")
                    st.write(f"**Autor:** {video_data.get('author', '')}")
                    st.write(f"**Publicado:** {video_data.get('publish_date', '')}")
                    st.write(f"**Views:** {video_data.get('views', 'N/A')}")
                    duracao = video_data.get('duration', 'N/A')
                    if isinstance(duracao, int):
                        minutes, seconds = divmod(duracao, 60)
                        hours, minutes = divmod(minutes, 60)
                        formatted_duration = f"{hours}h {minutes}m {seconds}s" if hours else f"{minutes}m {seconds}s"
                        st.write(f"**Duração:** {formatted_duration}")
                    tags = video_data.get('keywords', 'N/A')

                tab_summary, tab_topics, tab_article, tab_chat = st.tabs(["Summary", "Topics", "Article", "Chat"])

                with tab_summary:
                    st.markdown("<div class='summary-box'>" + analysis['summary'].replace(chr(10), '<br>') + "</div>", unsafe_allow_html=True)
                    st.download_button("Download Summary (.txt)", analysis['summary'], file_name="summary.txt")

                with tab_topics:
                    st.markdown(analysis['topics'])
                    st.download_button("Download Topics (.txt)", analysis['topics'], file_name="topics.txt")

                with tab_article:
                    current_article = None
                    if st.session_state.get('analysis') and st.session_state.analysis.get('article'):
                        current_article = st.session_state.analysis.get('article')
                    else:
                        current_article = analysis.get('article')
                    article_container = st.container()
                    article_container.empty()
                    article_container.markdown(current_article, unsafe_allow_html=True)
                    st.download_button("Download Article (.md)", current_article, file_name="article.md")

                with tab_chat:
                    vid = video_data.get('video_id')
                    chat_key = f'chat_history_{vid}'
                    if chat_key not in st.session_state:
                        st.session_state[chat_key] = []

                    st.markdown("#### Chat with the video (context-aware)")
                    st.info("You can ask questions about the video's title, description, tags, summary and transcript.")

                    for role, txt in st.session_state[chat_key]:
                        if role == 'user':
                            st.markdown(f"**You:** {txt}")
                        else:
                            st.markdown(f"**LLM:** {txt}")

                    input_key = f'chat_input_{vid}'
                    clear_key = f'clear_chat_{vid}'
                    default_val = None
                    if clear_key in st.session_state:
                        if input_key in st.session_state:
                            try:
                                del st.session_state[input_key]
                            except Exception:
                                pass
                        default_val = ''
                        try:
                            del st.session_state[clear_key]
                        except Exception:
                            pass

                    if default_val is not None:
                        question = st.text_input("Ask a question about this video:", value=default_val, key=input_key)
                    else:
                        question = st.text_input("Ask a question about this video:", key=input_key)

                    if st.button("Send", key=f'chat_send_{vid}') and question:
                        context_parts = []
                        if video_data.get('title'):
                            context_parts.append(f"Title: {video_data.get('title')}")
                        if video_data.get('description'):
                            context_parts.append(f"Description: {video_data.get('description')}")
                        if video_data.get('keywords'):
                            context_parts.append(f"Tags: {', '.join(video_data.get('keywords') if isinstance(video_data.get('keywords'), list) else [video_data.get('keywords')])}")
                        if analysis.get('summary'):
                            context_parts.append(f"Summary: {analysis.get('summary')}")
                        transcript = video_data.get('transcript') or ''
                        if transcript:
                            context_parts.append(f"Transcript excerpt: {transcript[:800]}")

                        context = "\n\n".join(context_parts)

                        prompt = f"Context:\n{context}\n\nUser question: {question}\n\nPlease answer concisely and reference the context when applicable."

                        llm = LLMService(
                            provider=st.session_state.llm_provider,
                            model_name=st.session_state.llm_model or None,
                            api_key=st.session_state.llm_api_key or None,
                            temperature=st.session_state.llm_temperature,
                            max_tokens=st.session_state.llm_max_tokens
                        )

                        with st.spinner("Asking LLM..."):
                            res = llm.generate(prompt)

                        if res and res.get('success'):
                            answer = res.get('text')
                            st.session_state[chat_key].append(('user', question))
                            st.session_state[chat_key].append(('assistant', answer))
                            st.session_state[clear_key] = True
                            st.rerun()
                        else:
                            st.error(f"LLM error: {res.get('error') if res else 'Unknown error'}")

                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🔄 Analisar Outro Vídeo", use_container_width=True):
                    self.reset()
                    st.rerun()
            else:
                st.error("❌ Análise não disponível. Por favor, tente novamente.")
                if st.button("← Voltar para a Página Inicial"):
                    self.reset()
                    st.rerun()

    def run(self):
        """Executa a interface principal"""
        
        st.markdown("""
            <div class="header-area">
                <h1>TubeTalk</h1>
                <h2>🤖 Your personal YouTube assistant</h2>
                <p>Analyze YouTube videos with AI-powered insights!</p>
                    
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<p style='text-align: center; margin-top: 0.5rem;'>Developed by <a href='https://www.linkedin.com/in/wellington-moreira-santos' target='_blank'>Wellington M Santos</a></p>", unsafe_allow_html=True)

        st.markdown("---")


        
        self.render_settings()

        if not st.session_state.submitted:
            st.markdown("<p style='font-size: 1.5rem; font-weight: bold; text-align: center;'>Insira uma URL de vídeo do YouTube para começar:</p>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 3, 1])
            with col2:
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
                    if url:
                        video_data = self.extract_transcript(url)

                        if video_data:
                            analysis = self.analyze_with_llm(video_data['transcript'], video_data)

                            if analysis:
                                st.session_state.video_data = video_data
                                st.session_state.analysis = analysis
                                st.session_state.submitted = True
                                st.session_state.analysis_complete = True
                                st.rerun()
                    else:
                        st.error("❌ Please enter a valid YouTube video URL.")
        else:
            if st.session_state.analysis_complete and st.session_state.video_data:
                video_data = st.session_state.video_data
                analysis = st.session_state.analysis

                st.markdown(f"### {video_data.get('title', '')}")
                col_thumb, col_meta = st.columns([2, 1])
                with col_thumb:
                    if video_data.get('thumbnail_url'):
                        st.image(video_data['thumbnail_url'], use_container_width=True)
                with col_meta:
                    st.write(f"**Canal:** {video_data.get('channel', '')}")
                    st.write(f"**Autor:** {video_data.get('author', '')}")
                    st.write(f"**Publicado:** {video_data.get('publish_date', '')}")
                    st.write(f"**Views:** {video_data.get('views', 'N/A')}")
                    duracao = video_data.get('duration', 'N/A')
                    if isinstance(duracao, int):
                        minutes, seconds = divmod(duracao, 60)
                        hours, minutes = divmod(minutes, 60)
                        formatted_duration = f"{hours}h {minutes}m {seconds}s" if hours else f"{minutes}m {seconds}s"
                        st.write(f"**Duração:** {formatted_duration}")
                    tags = video_data.get('keywords', 'N/A')

                tab_summary, tab_topics, tab_article, tab_chat = st.tabs(["Summary", "Topics", "Article", "Chat"])

                with tab_summary:
                    st.markdown("<div class='summary-box'>" + analysis['summary'].replace(chr(10), '<br>') + "</div>", unsafe_allow_html=True)
                    st.download_button("Download Summary (.txt)", analysis['summary'], file_name="summary.txt")

                with tab_topics:
                    st.markdown(analysis['topics'])
                    st.download_button("Download Topics (.txt)", analysis['topics'], file_name="topics.txt")

                with tab_article:
                    current_article = None
                    if st.session_state.get('analysis') and st.session_state.analysis.get('article'):
                        current_article = st.session_state.analysis.get('article')
                    else:
                        current_article = analysis.get('article')
                    article_container = st.container()
                    article_container.empty()
                    article_container.markdown(current_article, unsafe_allow_html=True)
                    st.download_button("Download Article (.md)", current_article, file_name="article.md")

                with tab_chat:
                    vid = video_data.get('video_id')
                    chat_key = f'chat_history_{vid}'
                    if chat_key not in st.session_state:
                        st.session_state[chat_key] = []

                    st.markdown("#### Chat with the video (context-aware)")
                    st.info("You can ask questions about the video's title, description, tags, summary and transcript.")

                    for role, txt in st.session_state[chat_key]:
                        if role == 'user':
                            st.markdown(f"**You:** {txt}")
                        else:
                            st.markdown(f"**LLM:** {txt}")

                    input_key = f'chat_input_{vid}'
                    clear_key = f'clear_chat_{vid}'
                    default_val = None
                    if clear_key in st.session_state:
                        if input_key in st.session_state:
                            try:
                                del st.session_state[input_key]
                            except Exception:
                                pass
                        default_val = ''
                        try:
                            del st.session_state[clear_key]
                        except Exception:
                            pass

                    if default_val is not None:
                        question = st.text_input("Ask a question about this video:", value=default_val, key=input_key)
                    else:
                        question = st.text_input("Ask a question about this video:", key=input_key)

                    if st.button("Send", key=f'chat_send_{vid}') and question:
                        context_parts = []
                        if video_data.get('title'):
                            context_parts.append(f"Title: {video_data.get('title')}")
                        if video_data.get('description'):
                            context_parts.append(f"Description: {video_data.get('description')}")
                        if video_data.get('keywords'):
                            context_parts.append(f"Tags: {', '.join(video_data.get('keywords') if isinstance(video_data.get('keywords'), list) else [video_data.get('keywords')])}")
                        if analysis.get('summary'):
                            context_parts.append(f"Summary: {analysis.get('summary')}")
                        transcript = video_data.get('transcript') or ''
                        if transcript:
                            context_parts.append(f"Transcript excerpt: {transcript[:800]}")

                        context = "\n\n".join(context_parts)

                        prompt = f"Context:\n{context}\n\nUser question: {question}\n\nPlease answer concisely and reference the context when applicable."

                        llm = LLMService(
                            provider=st.session_state.llm_provider,
                            model_name=st.session_state.llm_model or None,
                            api_key=st.session_state.llm_api_key or None,
                            temperature=st.session_state.llm_temperature,
                            max_tokens=st.session_state.llm_max_tokens
                        )

                        with st.spinner("Asking LLM..."):
                            res = llm.generate(prompt)

                        if res and res.get('success'):
                            answer = res.get('text')
                            st.session_state[chat_key].append(('user', question))
                            st.session_state[chat_key].append(('assistant', answer))
                            st.session_state[clear_key] = True
                            st.rerun()
                        else:
                            st.error(f"LLM error: {res.get('error') if res else 'Unknown error'}")

                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🔄 Analisar Outro Vídeo", use_container_width=True):
                    self.reset()
                    st.rerun()
            else:
                st.error("❌ Análise não disponível. Por favor, tente novamente.")
                if st.button("← Voltar para a Página Inicial"):
                    self.reset()
                    st.rerun()