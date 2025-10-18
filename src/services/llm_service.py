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
		self.llm = self._initialize_llm()

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

	def _initialize_llm(self):
		""" Inicializa o modelo LLM no provedor escolhido"""

		try:
			if self.provider=='openai':
				if not self.api_key: raise ValueError("Requer API KEY OpenAI")
				model = self.model_name or 'gpt-3.5-turbo'
				return ChatOpenAI(
					model = model,
					temperature = self.temperature,
					max_tokens = self.max_tokens,
					api_key = self.api_key
					)
			elif self.provider=='ollama':
				model = self.model_name or 'phi3'
				return Ollama(model=model, temperature=self.temperature)
			elif self.provider=='groq':
				if not self.api_key:raise ValueError("Requer API KEY Groq")
				model = self.model_name or 'llama-3.3-70b-versatile'
				return ChatGroq(
					model=model,
					temperature=self.temperature,
					max_tokens=self.max_tokens,
					api_key=self.api_key
					)
			elif self.provider=='huggingface':
				if not self.api_key:raise ValueError("Requer API Key Huggingace")
				model = self.model_name or 'phi3'
				return HuggingFaceHub(
					repo_id=model,
					model_kwargs={
						'temperature':self.temperature,
						'max_length':self.max_tokens
					},
					huggingface_api_token=self.api_key
					)
			else: 
				raise ValueError(f"Provedor de LLM não suportado: {self.provider}")
		except Exception as e:
			raise Exception(f"Falha ao iniciar LLM: {e}")

	def generate(self, prompt:str) -> Dict[str, any]:
		""" Gera texto usando LLM """

		try:
			if hasattr(self.llm, 'invoke'):
				response = self.llm.invoke(prompt)
				text = response.content if hasattr(response, 'content') else str(response)
			else:text=self.llm(prompt)
			return {
			'success':True,
			'text': text.strip(),
			'error':None
			}
		except Exception as e:
			return {
			'success':False,
			'text': None,
			'error':f"Falha ao gerar texto: {e}"
			}

	def generate_summary(
		self, 
		transcript:str,
		prompt_template:str
		) -> Dict[str, any]:

		"""Gera um resumo da trancrição"""

		try:
			prompt = prompt_template.format(transcript=transcript)
			result = self.generate(prompt)

			if result['success']:
				return {
					'success':True,
					'summary': result['text'],
					'error':None
				}
			else:return result
		except Exception as e:
			return {
				'success':False,
				'summary':None,
				'error': f'Falha ao gerar sumario: {e}'
			}
	
	def extract_topics(
		self,
		transcript:str,
		prompt_template:str
		) -> Dict[str, any]:

		""" Extrai tópicos chave da trancrição """

		try:
			prompt = prompt_template.format(transcript=transcript)
			result = self.generate(prompt)

			if result['success']:
				return {
					'success':True,
					'topics': result['text'],
					'error':None
				}
			else:return result
		except Exception as e:
			return {
				'success':False,
				'topics':None,
				'error': f'Falha ao extrair tópicos: {e}'
			}

	def generate_article(
		self,
		transcript: str,
		title: Optional[str]=None,
		prompt_template: Optional[str]=None,
		length: str = 'medium'  # 'short'|'medium'|'long'
		) -> Dict[str, any]:
		"""
		Gera um artigo baseado na transcrição.

		Args:
			transcript: Texto da transcrição
			title: Título opcional para o artigo
			prompt_template: Template de prompt (se não fornecido, usa um padrão)
			length: Tamanho desejado do artigo ('short','medium','long')

		Returns:
			Dict com 'success', 'article' e 'error'
		"""

		try:
			if not transcript or transcript.strip() == '':
				return {'success': False, 'article': None, 'error': 'Transcript vazio'}

			# Prompt padrão
			default_prompt = (
				"Escreva um artigo bem estruturado com base na transcrição abaixo. "
				"Inclua uma introdução, subtítulos quando apropriado e uma conclusão. "
				"Use um tom informativo e claro.\n\nTranscrição:\n{transcript}\n\n" 
			)

			# Ajusta extensão esperada
			if length == 'short':
				length_hint = 'Escreva um artigo curto, aproximando-se de 150-300 palavras.'
			elif length == 'long':
				length_hint = 'Escreva um artigo longo e detalhado, aproximando-se de 800-1200 palavras.'
			else:
				length_hint = 'Escreva um artigo de média extensão, aproximando-se de 400-700 palavras.'

			# Constrói o prompt final
			prompt_base = prompt_template or default_prompt
			if title:
				prompt_full = f"Escreva um artigo em português pt-BR intitulado '{title}'. {length_hint}\n\n" + prompt_base.format(transcript=transcript, title=title)
			else:
				prompt_full = length_hint + "\n\n" + prompt_base.format(transcript=transcript, title="")

			# Gera com o LLM
			result = self.generate(prompt_full)
			if result['success']:
				return {'success': True, 'article': result['text'], 'error': None}
			else:
				return result

		except Exception as e:
			return {'success': False, 'article': None, 'error': f'Falha ao gerar artigo: {e}'}
	
	@staticmethod
	def validate_config(
		provider:str,
		api_key:Optional[str]=None
		) -> Dict[str, any]:
		""" Valida a configuração do provedor """

		if provider not in LLMService.PROVIDERS_MAP:
			return {
				'valid':False,
				'error':f"Provedor inválido: {provider}"
			}
		if provider=='ollama':
			return {'valid':True, 'error':None}

		env_key_map = {
			'openai':os.getenv('OPENAI_API_KEY'),
			'groq':os.getenv('GROQ_API_KEY'),
			'huggingface':os.getenv('HUGGINGFACEHUB_API_KEY'),
		}

		has_env_key = env_key_map.get(provider) is not None
		has_provided_key = api_key is not None and api_key.strip() != ''

		if has_env_key or has_provided_key:
			return {'valid':True, 'error':None}
		else:
			return {
				'valid':False,
				'error':f"Falta API Key para o provedor {provider}"
			}