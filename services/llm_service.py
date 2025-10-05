"""
Serviço para processamento de transcrições usando diferentes modelos de LLMs
"""

import os
from typing import Dict, Optional
from dotenv import load_dotenv

try:
	from langchain_community.llms import Ollama
	from langchain_community.llms import HuggingFaceHub
	from langchain_openai import ChatOpenAI
	from langchain_groq import ChatGroq
	from langchain.prompts import PromptTemplate
	from langchain.chains import LLMChain
except ImportError as e:
	print( f'Faltam dependências Langchain: {e}' )

load_dotenv()

class LLMService:
	"""Serviço para processar trancrições usando LLMs"""

	PROVIDERS_MAP = {
		'openai':'OpenAI',
		'ollama':'Ollama',
		'groq':'Groq',
		'huggingface':'huggingface',
	}

	def __init__(
		self,
		provider:str = 'openai',
		model_name:Optional[str]=None,
		api_key:Optional[str]=None,
		temperature:float = 0.7,
		max_tokens:int = 1000,):

		self.provider = provider.lower()
		self.model_name = model_name
		self.temperature = temperature
		self.max_tokens = max_tokens
		self.api_key = self._get_api_key(provider=provider, provided_key=api_key)

		# implementar inicialização de llm
		# self.llm = ...

	def _get_api_key(
		self,
		provider:str,
		provided_key:Optional[str]=None
		) -> Optional[str]:
		""" Método que obtém a API Key """

		if provider == 'ollama':return None

		env_key_map = {
			'openai':'OPENAI_API_KEY',
			'groq':'GROQ_API_KEY',
			'huggingface':'HUGGINGFACEHUB_API_KEY',
		}
		env_key = env_key_map.get(provider)

		if env_key:
			api_key = os.getenv(env_key)
			if api_key: return api_key

		return provided_key

