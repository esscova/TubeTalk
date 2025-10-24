# Documentação do Módulo `ui.py`

Este documento descreve o módulo `ui.py`, que implementa a interface de usuário principal para o aplicativo **TubeTalk**, utilizando a biblioteca Streamlit. Ele integra os serviços `YouTubeService` e `LLMService` para analisar vídeos do YouTube, exibindo metadados, resumos, tópicos, artigos gerados e permitindo interações via chat com contexto.

## Visão Geral

O módulo `ui.py` contém a classe `UI`, que gerencia a interface web do aplicativo TubeTalk. A interface permite aos usuários inserir URLs de vídeos do YouTube, configurar provedores de LLM, visualizar análises (resumo, tópicos e artigo) e interagir com o vídeo por meio de um chat contextual. A interface é estilizada com CSS personalizado e utiliza o gerenciamento de estado do Streamlit para persistência de dados durante a interação.

## Dependências

- `streamlit`: Para construção da interface web interativa.
- `services`: Módulos `YouTubeService` e `LLMService` para extração de dados de vídeos e processamento de texto com LLMs.
- `configs.prompts`: Contém templates de prompts (`SUMMARY_PROMPT_TEMPLATE`, `TOPICS_PROMPT_TEMPLATE`, `ARTICLE_PROMPT_TEMPLATE`) usados para gerar análises.

## Estrutura do Módulo

### Classe `UI`

#### `__init__(self)`

Inicializa a interface, configurando estados iniciais no `st.session_state` do Streamlit e definindo estilos CSS personalizados.

- **Estados gerenciados**:
  - `submitted`: Indica se uma URL de vídeo foi enviada (`False` por padrão).
  - `video_url`: URL do vídeo inserida pelo usuário.
  - `video_data`: Dados do vídeo extraídos por `YouTubeService`.
  - `analysis_complete`: Indica se a análise do vídeo foi concluída.
  - `analysis`: Resultados da análise (resumo, tópicos, artigo).
  - `llm_provider`: Provedor de LLM selecionado (padrão: `'openai'`).
  - `llm_model`: Nome do modelo LLM.
  - `llm_api_key`: Chave de API para o provedor de LLM.
  - `llm_temperature`: Temperatura do LLM (padrão: `0.7`).
  - `llm_max_tokens`: Máximo de tokens para respostas do LLM (padrão: `1000`).
- **Estilos CSS**:
  - `header-area`: Cabeçalho com gradiente.
  - `video-section`: Seções de vídeo com fundo estilizado.
  - `info-card`: Cartões de informação com borda colorida.
  - `summary-box`: Caixa de resumo com borda destacada.

#### `reset(self)`

Redefine os estados da sessão para os valores iniciais, permitindo a análise de um novo vídeo.

#### `get_default_model(self, provider: str) -> str`

Retorna o modelo padrão para um provedor de LLM.

- **Parâmetros**:
  - `provider`: Provedor de LLM (`openai`, `ollama`, `groq`, `huggingface`).
- **Retorno**:
  - String com o nome do modelo padrão:
    - `openai`: `gpt-3.5-turbo`
    - `ollama`: `llama2`
    - `groq`: `llama-3.3-70b-versatile`
    - `huggingface`: `mistralai/Mistral-7B-Instruct-v0.1`
    - Retorna `''` para provedores inválidos.

#### `render_settings(self)`

Renderiza a barra lateral com configurações do LLM.

- **Funcionalidades**:
  - Seleção do provedor de LLM via `st.selectbox`.
  - Campo para nome do modelo com placeholder do modelo padrão.
  - Campo para chave de API (exceto para Ollama).
  - Validação da configuração do LLM usando `LLMService.validate_config`.
  - Sliders para ajustar `temperature` (0.0 a 1.0) e `max_tokens` (100 a 1000).
  - Botão para testar a configuração do LLM (`_test_llm`).

#### `_test_llm(self)`

Testa a configuração do LLM enviando um prompt simples ("Diga 'ok'").

- **Lógica**:
  - Instancia `LLMService` com as configurações atuais.
  - Exibe mensagem de sucesso ou erro com base na resposta do LLM.
  - Ajusta a exibição de mensagens longas para a barra lateral.

#### `extract_transcript(self, url: str)`

Extrai metadados e transcrição de um vídeo do YouTube.

- **Parâmetros**:
  - `url`: URL do vídeo do YouTube.
- **Retorno**:
  - Dados do vídeo (via `YouTubeService.get_complete_data`) ou `None` em caso de erro.
- **Comportamento**:
  - Exibe um spinner durante a extração.
  - Mostra erro se a extração falhar.

#### `analyze_with_llm(self, transcript: str, video_data: dict = None)`

Realiza análise do vídeo usando o LLM configurado.

- **Parâmetros**:
  - `transcript`: Texto da transcrição do vídeo.
  - `video_data`: Dados do vídeo (opcional, usado para contexto).
- **Retorno**:
  - Dicionário com:
    - `summary`: Resumo gerado.
    - `topics`: Tópicos extraídos.
    - `article`: Artigo gerado.
    - Retorna `None` em caso de erro.
- **Lógica**:
  - Instancia `LLMService` com configurações atuais.
  - Gera resumo, tópicos e artigo usando templates de prompt.
  - Exibe erros específicos para cada etapa e sugere soluções.

#### `render_video_analysis(self, video_data: dict, analysis: dict)`

Renderiza a análise do vídeo (usado em versões anteriores; substituído por lógica em `run`).

- **Parâmetros**:
  - `video_data`: Dados do vídeo.
  - `analysis`: Resultados da análise (resumo, tópicos, artigo).
- **Funcionalidades**:
  - Exibe o vídeo em um iframe do YouTube.
  - Mostra metadados (título, autor, canal, data, visualizações, curtidas, palavras-chave).
  - Apresenta resumo, tópicos e artigo em seções estilizadas.

#### `run(self)`

Executa a interface principal do aplicativo.

- **Funcionalidades**:
  - Exibe cabeçalho com título, subtítulo e crédito ao desenvolvedor.
  - Renderiza configurações do LLM na barra lateral.
  - **Estado inicial (`submitted=False`)**:
    - Solicita a URL do vídeo em um campo de entrada.
    - Botão "Analisar Vídeo" inicia a extração e análise.
    - Exibe erro se a URL estiver vazia.
  - **Estado após análise (`submitted=True`)**:
    - Exibe título do vídeo e metadados (thumbnail, canal, autor, data, visualizações, duração).
    - Apresenta resultados em abas:
      - **Summary**: Resumo com botão de download (`.txt`).
      - **Topics**: Tópicos com botão de download (`.txt`).
      - **Article**: Artigo com botão de download (`.md`).
      - **Chat**: Interface de chat contextual com histórico.
    - Botão "Analisar Outro Vídeo" reinicia o processo.
  - **Chat**:
    - Permite perguntas sobre o vídeo (título, descrição, tags, resumo, transcrição).
    - Constrói contexto a partir dos dados do vídeo.
    - Mantém histórico de conversa por vídeo (`chat_history_{video_id}`).
    - Botão "Send" envia perguntas ao LLM e atualiza o histórico.

## Exemplo de Uso

```python
from ui import UI

# Inicializa e executa a interface
ui = UI()
ui.run()
```

## Notas

- A interface usa `st.session_state` para manter o estado entre interações.
- O chat é contextual, usando título, descrição, tags, resumo e um trecho da transcrição (até 800 caracteres).
- Os resultados podem ser baixados como arquivos de texto ou Markdown.
- A estilização CSS melhora a experiência visual com gradientes e caixas destacadas.
- O módulo assume que os templates de prompt estão definidos em `configs.prompts`.

## Limitações

- Depende da correta configuração do LLM e da disponibilidade da API do YouTube.
- O chat usa apenas os primeiros 800 caracteres da transcrição para evitar excesso de contexto.
- Erros de API ou configurações inválidas são exibidos com sugestões de solução.
- Não há suporte para múltiplos vídeos simultaneamente na mesma sessão.

## Possíveis Melhorias

- Adicionar suporte para múltiplos vídeos na mesma sessão.
- Implementar opções de personalização de prompts na interface.
- Melhorar o chat com suporte a contextos mais longos ou busca por trechos específicos.
- Adicionar visualizações gráficas (ex.: nuvem de palavras para tópicos).
- Incluir opção para salvar/exportar análises completas como PDF.