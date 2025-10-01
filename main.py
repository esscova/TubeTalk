# DEPENDENCIAS
import streamlit as st
import resquests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

from langchain_community.document_loaders import YoutubeLoader
from langchain_community.tools import YoutubeSearchTool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.huggingface_hub import HuggingFaceEmbeddings, HuggingFaceEndpoint
from langchain.vectorstores import FAISS

# CONFIGS
## variaveis
load_dotenv()

HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
HUGGINGFACEHUB_API_URL = os.getenv("HUGGINGFACEHUB_API_URL")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

## streamlit
st.set_page_config(page_title="YouTube GPT", page_icon=":robot_face:")
st.header("YouTube GPT :robot_face:")
st.markdown("### Ferramenta de busca e resumo de vídeos do YouTube utilizando IA")

## iniciando tools
youtube_search = YoutubeSearchTool(api_key=YOUTUBE_API_KEY)

# FUNÇÕES
## modelo huggingface
def model_hf_hub(model='microsoft/Phi-3-mini-4-instruct', temperature=0.1, max_new_tokens=1024):
    """Função para iniciar o modelo HuggingFaceHub"""
    endpoint = HUGGINGFACEHUB_API_URL
    api_token = HUGGINGFACEHUB_API_TOKEN
    llm = HuggingFaceEndpoint(
        endpoint_url=endpoint,
        task="text-generation",
        model=model,
        temperature=temperature,
        max_new_tokens=max_new_tokens,
        api_key=api_token
    )
    return llm