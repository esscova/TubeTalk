# Documentação do Módulo `llm_service.py`

Este documento descreve o módulo `llm_service.py`, que fornece um serviço para processamento de transcrições utilizando diferentes modelos de Language Models (LLMs) de provedores como OpenAI, Groq, Ollama e HuggingFace.

## Visão Geral

O módulo `llm_service.py` contém a classe `LLMService`, que permite processar transcrições de texto para gerar resumos, extrair tópicos-chave e criar artigos completos com base em prompts personalizáveis. Ele suporta múltiplos provedores de LLMs e é configurável para diferentes modelos, temperaturas e tamanhos máximos de tokens.

## Dependências

- `os`: Para manipulação de variáveis de ambiente.
- `dotenv`: Para carregar variáveis de ambiente de um arquivo `.env`.
- `typing`: Para anotações de tipo.
- `langchain_community.llms`: Para integração com Ollama e HuggingFace.
- `langchain_openai`: Para integração com OpenAI.
- `langchain_groq`: Para integração com Groq.
- `langchain.prompts`: Para criação de templates de prompts.
- `langchain.chains`: Para execução de cadeias de prompts com LLMs.

## Estrutura do Módulo

### Classe `LLMService`

#### `PROVIDERS_MAP`

Dicionário estático que mapeia os provedores suportados:

- `openai`: OpenAI
- `ollama`: Ollama
- `groq`: Groq
- `huggingface`: HuggingFace

#### `__init__(self, provider: str = 'openai', model_name: Optional[str] = None, api_key: Optional[str] = None, temperature: float = 0.7, max_tokens: int = 1000)`

Inicializa o serviço com configurações para o provedor de LLM.

- **Parâmetros**:
  - `provider`: Provedor do LLM (padrão: `'openai'`).
  - `model_name`: Nome do modelo (opcional; se não fornecido, usa um padrão por provedor).
  - `api_key`: Chave de API (opcional; se não fornecido, busca em variáveis de ambiente).
  - `temperature`: Controla a criatividade do modelo (padrão: `0.7`).
  - `max_tokens`: Número máximo de tokens na resposta (padrão: `1000`).
- **Função**: Configura o provedor, modelo e inicializa o LLM.

#### `_get_api_key(self, provider: str, provided_key: Optional[str] = None) -> Optional[str]`

Obtém a chave de API para o provedor.

- **Parâmetros**:
  - `provider`: Provedor do LLM.
  - `provided_key`: Chave de API fornecida (opcional).
- **Retorno**:
  - String com a chave de API ou `None` (para Ollama, que não requer chave).
- **Lógica**:
  - Verifica variáveis de ambiente (`OPENAI_API_KEY`, `GROQ_API_KEY`, `HUGGINGFACEHUB_API_KEY`).
  - Retorna a chave fornecida se disponível e válida, caso contrário, usa a variável de ambiente.

#### `_initialize_llm(self)`

Inicializa o modelo LLM com base no provedor.

- **Retorno**:
  - Instância do modelo configurado (`ChatOpenAI`, `Ollama`, `ChatGroq` ou `HuggingFaceHub`).
- **Modelos padrão**:
  - OpenAI: `gpt-3.5-turbo`
  - Ollama: `phi3`
  - Groq: `llama-3.3-70b-versatile`
  - HuggingFace: `phi3`
- **Exceções**:
  - Levanta `ValueError` se a chave de API for necessária e não fornecida.
  - Levanta `Exception` para falhas genéricas na inicialização.

#### `generate(self, prompt: str) -> Dict[str, any]`

Gera texto usando o LLM configurado.

- **Parâmetros**:
  - `prompt`: Texto do prompt a ser processado.
- **Retorno**:
  - Dicionário com:
    - `success` (bool): Indica se a operação foi bem-sucedida.
    - `text` (str): Texto gerado ou `None` se falhar.
    - `error` (str): Mensagem de erro ou `None` se bem-sucedido.
- **Exceções**:
  - Captura erros do LLM e retorna no campo `error`.

#### `generate_summary(self, transcript: str, prompt_template: str) -> Dict[str, any]`

Gera um resumo de uma transcrição.

- **Parâmetros**:
  - `transcript`: Texto da transcrição.
  - `prompt_template`: Template de prompt com espaço reservado `{transcript}`.
- **Retorno**:
  - Dicionário com:
    - `success` (bool): Indica se a operação foi bem-sucedida.
    - `summary` (str): Resumo gerado ou `None` se falhar.
    - `error` (str): Mensagem de erro ou `None` se bem-sucedido.
- **Exceções**:
  - Captura erros e retorna no campo `error`.

#### `extract_topics(self, transcript: str, prompt_template: str) -> Dict[str, any]`

Extrai tópicos-chave de uma transcrição.

- **Parâmetros**:
  - `transcript`: Texto da transcrição.
  - `prompt_template`: Template de prompt com espaço reservado `{transcript}`.
- **Retorno**:
  - Dicionário com:
    - `success` (bool): Indica se a operação foi bem-sucedida.
    - `topics` (str): Tópicos extraídos ou `None` se falhar.
    - `error` (str): Mensagem de erro ou `None` se bem-sucedido.
- **Exceções**:
  - Captura erros e retorna no campo `error`.

#### `generate_article(self, transcript: str, title: Optional[str] = None, prompt_template: Optional[str] = None, length: str = 'medium') -> Dict[str, any]`

Gera um artigo baseado em uma transcrição.

- **Parâmetros**:
  - `transcript`: Texto da transcrição.
  - `title`: Título opcional para o artigo.
  - `prompt_template`: Template de prompt personalizado (opcional; usa um padrão se não fornecido).
  - `length`: Tamanho do artigo (`'short'`, `'medium'`, `'long'`; padrão: `'medium'`).
- **Retorno**:
  - Dicionário com:
    - `success` (bool): Indica se a operação foi bem-sucedida.
    - `article` (str): Artigo gerado ou `None` se falhar.
    - `error` (str): Mensagem de erro ou `None` se bem-sucedido.
- **Lógica**:
  - Usa um prompt padrão se nenhum for fornecido.
  - Ajusta o comprimento do artigo: curto (150-300 palavras), médio (400-700 palavras), longo (800-1200 palavras).
  - Realiza pós-processamento para remover prefixos indesejados (ex.: `Meta description:`) e garantir capitalização inicial.
- **Exceções**:
  - Retorna erro se a transcrição estiver vazia.

#### `validate_config(provider: str, api_key: Optional[str] = None) -> Dict[str, any]`

Valida a configuração do provedor.

- **Parâmetros**:
  - `provider`: Provedor do LLM.
  - `api_key`: Chave de API fornecida (opcional).
- **Retorno**:
  - Dicionário com:
    - `valid` (bool): Indica se a configuração é válida.
    - `error` (str): Mensagem de erro ou `None` se válida.
- **Lógica**:
  - Verifica se o provedor é suportado.
  - Para Ollama, não requer chave de API.
  - Para outros provedores, verifica a existência de chave de API em variáveis de ambiente ou fornecida diretamente.

## Exemplo de Uso

```python
from llm_service import LLMService

# Inicializa o serviço com Groq
service = LLMService(provider="groq", model_name="llama-3.3-70b-versatile", api_key="sua-chave-aqui")

# Exemplo de transcrição
transcript = "Este é um texto de exemplo sobre inteligência artificial e seus impactos na sociedade..."

# Template de prompt para resumo
summary_prompt = "Resuma o seguinte texto em 3-5 frases: {transcript}"

# Gera um resumo
summary_result = service.generate_summary(transcript, summary_prompt)
if summary_result['success']:
    print(f"Resumo: {summary_result['summary']}")
else:
    print(f"Erro: {summary_result['error']}")

# Gera um artigo
article_result = service.generate_article(transcript, title="Impactos da IA", length="medium")
if article_result['success']:
    print(f"Artigo: {article_result['article'][:200]}...")
else:
    print(f"Erro: {article_result['error']}")
```

## Notas

- O módulo requer configuração de chaves de API em um arquivo `.env` ou fornecidas diretamente, exceto para Ollama.
- O pós-processamento em `generate_article` remove prefixos indesejados comuns em respostas de LLMs.
- Os métodos retornam dicionários padronizados com campos `success` e `error` para facilitar o tratamento de erros.

## Limitações

- Depende da disponibilidade dos provedores de LLM e suas APIs.
- O desempenho pode variar dependendo do modelo e provedor escolhidos.
- Requer instalação das bibliotecas LangChain específicas para cada provedor.

## Possíveis Melhorias

- Adicionar suporte a mais provedores de LLMs.
- Implementar cache para respostas frequentes.
- Suportar prompts em outros idiomas além do português.
- Adicionar validação mais robusta para transcrições vazias ou malformadas.