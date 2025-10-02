# DEPENDENCIAS
import streamlit as st
import requests
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
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint
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

## informações do vídeo
### titulo
def get_video_title(video_url):
    """Função para extrair o título do vídeo a partir da URL"""
    try:
        response = requests.get(video_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('meta', property='og:title')
        if title:
            return title['content']
        return "Título não encontrado"
    
    except Exception as e:
        return f"Erro ao buscar título: {e}"
    
### informações gerais e transcrição
def get_video_info(video_url, language=['pt', 'pt-BR', 'en', 'en-US'], translate=None):
    """Função para extrair informações e transcrição do vídeo a partir da URL"""
    try:
        video_id = video_url.split("v=")[-1]
        result = YouTubeTranscriptApi.fetch(video_id, languages=language, translate=translate)
        formatter = TextFormatter()
        transcript = formatter.format_transcript(result).replace("\n", " ")
        title = get_video_title(video_url)
        return transcript, title
    
    except Exception as e:
        return f"Erro ao buscar informações do vídeo: {e}"
    
## vetorização
def create_vector_store(transcript):
    """Função para criar o vetor a partir da transcrição"""
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = text_splitter.create_documents([transcript])
        
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"}
        )
        
        vector_store = FAISS.from_documents(docs, embeddings)
        return vector_store
    
    except Exception as e:
        return f"Erro ao criar vetor: {e}"
    
## langchain pipeline
def llm_chain(model='hf_hub'):
    """Função para criar o pipeline do LangChain"""
    try:
        system_prompt = """Você é um assistente virtual prestativo. Responda em português, de forma clara e concisa, com base no contexto fornecido da transcrição de um vídeo."""
        inputs = "Contexto: {context}\nConsulta: {consulta}"

        if model.startswith('hf_hub'):
            user_prompt = "<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n{}\n<|eot_id|><|start_header_id|>assistant<|end_header_id|>".format(inputs)
        else:
            user_prompt = inputs
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", user_prompt)
        ])

        llm = model_hf_hub()
        chain = prompt | llm | StrOutputParser()
        return chain
    
    except Exception as e:
        return f"Erro ao criar pipeline: {e}"
    
## resumo
def get_summary(chain, vector_store, query, k=4):
    """Função para obter o resumo a partir do vetor e da consulta"""
    try:
        docs = vector_store.similarity_search(query, k=k)
        context = "\n".join([doc.page_content for doc in docs])
        response = chain.invoke({"context": context, "consulta": query})
        return response['text']
    
    except Exception as e:
        return f"Erro ao obter resumo: {e}"