# Documentação do Módulo `youtube_service.py`

Este documento descreve o módulo `youtube_service.py`, que fornece um serviço para extrair transcrições e informações de vídeos do YouTube utilizando as bibliotecas `youtube_transcript_api` e `yt_dlp`.

## Visão Geral

O módulo `youtube_service.py` contém a classe `YouTubeService`, que permite interagir com vídeos do YouTube para obter transcrições e metadados detalhados, como título, autor, data de publicação, visualizações, duração, entre outros. Ele suporta a extração de IDs de vídeos a partir de URLs, formatação de transcrições, e recuperação de informações detalhadas usando a biblioteca `yt_dlp`.

## Dependências

- `youtube_transcript_api`: Para obter transcrições de vídeos.
- `yt_dlp`: Para extrair metadados de vídeos do YouTube.
- `datetime`: Para manipulação de datas.
- `typing`: Para anotações de tipo.

## Estrutura do Módulo

### Classe `YouTubeService`

#### `__init__(self, languages: list = None)`

Inicializa o serviço com uma lista de idiomas preferidos para transcrições.

- **Parâmetros**:
  - `languages` (opcional): Lista de códigos de idioma (ex.: `["pt", "pt-BR", "en", "en-US"]`). Se não fornecido, usa uma lista padrão com esses idiomas.
- **Função**: Configura as preferências de idioma para transcrições.

#### `extract_video_id(url: str) -> Optional[str]`

Extrai o ID do vídeo a partir de uma URL do YouTube.

- **Parâmetros**:
  - `url`: URL do vídeo do YouTube (ex.: `https://www.youtube.com/watch?v=Sm5jALppTLE` ou `https://youtu.be/Sm5jALppTLE`).
- **Retorno**:
  - String com o ID do vídeo (11 caracteres) ou `None` se a URL for inválida.
- **Exceções**:
  - Retorna `None` em caso de erro ou URL inválida.

#### `get_transcript(video_url: str) -> Dict[str, any]`

Obtém a transcrição de um vídeo do YouTube.

- **Parâmetros**:
  - `video_url`: URL do vídeo do YouTube.
- **Retorno**:
  - Dicionário com:
    - `success` (bool): Indica se a operação foi bem-sucedida.
    - `transcript` (str): Texto da transcrição ou `None` se falhar.
    - `language` (str): Idioma da transcrição ou `None` se falhar.
    - `is_generated` (bool): Indica se a transcrição é gerada automaticamente.
    - `error` (str): Mensagem de erro ou `None` se bem-sucedido.
- **Exceções**:
  - Captura erros da API de transcrição e retorna no campo `error`.

#### `get_video_info(video_url: str) -> Dict[str, any]`

Obtém metadados detalhados do vídeo usando `yt_dlp`.

- **Parâmetros**:
  - `video_url`: URL do vídeo do YouTube.
- **Retorno**:
  - Dicionário com:
    - `success` (bool): Indica se a operação foi bem-sucedida.
    - `video_id` (str): ID do vídeo.
    - `title` (str): Título do vídeo.
    - `author` (str): Nome do autor/uploader.
    - `channel` (str): Nome do canal.
    - `publish_date` (datetime.date): Data de publicação ou `None`.
    - `views` (int): Número de visualizações.
    - `likes` (int): Número de curtidas.
    - `duration` (int): Duração em segundos.
    - `description` (str): Descrição do vídeo.
    - `thumbnail_url` (str): URL da miniatura.
    - `keywords` (list): Lista de palavras-chave/tags.
    - `rating` (float): Avaliação média.
    - `category` (str): Categoria do vídeo ou `None`.
    - `error` (str): Mensagem de erro ou `None` se bem-sucedido.
- **Exceções**:
  - Captura erros do `yt_dlp` e retorna no campo `error`.

#### `get_complete_data(video_url: str) -> Dict[str, any]`

Combina transcrição e metadados do vídeo em uma única chamada.

- **Parâmetros**:
  - `video_url`: URL do vídeo do YouTube.
- **Retorno**:
  - Dicionário com todos os campos de `get_video_info` e `get_transcript`, incluindo:
    - `transcript` (str): Texto da transcrição.
    - `transcript_language` (str): Idioma da transcrição.
    - `transcript_is_generated` (bool): Indica se a transcrição é gerada automaticamente.
    - `error` (str): Mensagem de erro ou `None`.
- **Comportamento**:
  - Primeiro chama `get_video_info`. Se falhar, retorna o erro imediatamente.
  - Em seguida, chama `get_transcript` e combina os resultados.

#### `format_duration(seconds: int) -> str`

Formata a duração do vídeo de segundos para o formato `HH:MM:SS` ou `MM:SS`.

- **Parâmetros**:
  - `seconds`: Duração em segundos.
- **Retorno**:
  - String formatada (ex.: `"1:05:45"` ou `"10:30"`) ou `"N/A"` se `seconds` for inválido.

#### `format_views(views: int) -> str`

Formata o número de visualizações para um formato legível.

- **Parâmetros**:
  - `views`: Número de visualizações.
- **Retorno**:
  - String formatada (ex.: `"1.2M"`, `"450K"`, `"150"`) ou `"N/A"` se `views` for inválido.

## Exemplo de Uso

```python
from youtube_service import YouTubeService

# Inicializa o serviço
service = YouTubeService()

# URL de exemplo
url = "https://www.youtube.com/watch?v=Sm5jALppTLE"

# Obtém dados completos
data = service.get_complete_data(url)

if data['success']:
    print(f"Título: {data['title']}")
    print(f"Autor: {data['author']}")
    print(f"Duração: {YouTubeService.format_duration(data['duration'])}")
    print(f"Visualizações: {YouTubeService.format_views(data['views'])}")
    print(f"Idioma da transcrição: {data['transcript_language']}")
    print(f"Transcrição: {data['transcript'][:200]}...")
else:
    print(f"Erro: {data['error']}")
```

## Notas

- O módulo suporta URLs no formato `youtube.com/watch?v=ID` e `youtu.be/ID`.
- A transcrição é retornada como uma string única, com quebras de linha substituídas por espaços.
- O idioma da transcrição segue a ordem de preferência definida em `languages`.
- Para vídeos sem transcrição disponível, o método `get_transcript` retorna um erro no campo `error`.
- O módulo não realiza download de vídeos, apenas extrai metadados e transcrições.

## Limitações

- Depende da disponibilidade da API de transcrições do YouTube.
- Algumas informações (ex.: curtidas, avaliações) podem não estar disponíveis dependendo das restrições do vídeo.
- URLs inválidas ou vídeos privados podem resultar em erros.

## Possíveis Melhorias

- Adicionar suporte a mais formatos de transcrição (ex.: SRT, JSON).
- Implementar cache para evitar chamadas repetidas à API.
- Adicionar tratamento para vídeos com restrição de idade ou região.