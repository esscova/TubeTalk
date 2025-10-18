"""
Configurações de prompts para o serviço de LLM
"""

SUMMARY_PROMPT_TEMPLATE = """Por favor, leia a transcrição abaixo e escreva um único parágrafo curto (2-4 frases) que apresente de forma clara e concisa sobre o que trata o vídeo. O parágrafo deve ser informativo, em tom neutro, e servir como uma introdução explicativa para leitores que ainda não assistiram ao vídeo.

Transcrição:
{transcript}

Parágrafo introdutório:"""

TOPICS_PROMPT_TEMPLATE = """Você é um assistente que identifica os tópicos mais importantes de uma transcrição de vídeo.

Instruções:
- Analise a transcrição abaixo e extraia os 3 a 5 tópicos MAIS RELEVANTES, ordenados por importância.
- Para cada tópico, produza uma linha no formato: "- Título curto: Uma frase que resume o que foi discutido sobre esse tópico."
- Use títulos de 2 a 5 palavras (curtos) e descrições de no máximo 20 palavras.
- Não inclua explicações adicionais; apenas a lista de tópicos.

TRANSCRIÇÃO:
{transcript}

SAÍDA (exatamente neste formato):
- Tópico 1: Descrição breve de 1-2 frases
- Tópico 2: Descrição breve de 1-2 frases
- Tópico 3: Descrição breve de 1-2 frases
"""

ARTICLE_PROMPT_TEMPLATE = """
Você é um redator experiente em transformar transcrições em artigos otimizados para web.

Instruções claras:
- Leia atentamente a transcrição fornecida e NÃO copie trechos literalmente; reescreva com suas próprias palavras mantendo a ideia central.
- Se um título (`{title}`) for fornecido, use-o como título do artigo; caso contrário, sugira um título curto e direto.
- Gere também uma meta description de até 160 caracteres.
- Estruture o artigo assim:
    1) Título (H1)
    2) Escreva aqui a Meta description naturalmente chamando a atenção do leitor (uma linha)
    3) Introdução curta (1-2 parágrafos curtos)
    4) 2 a 4 subseções (H2) com subtítulos claros e 1-2 parágrafos explicativos cada
    5) Conclusão curta (1 parágrafo) com principais takeaways

- Mantenha um tom informativo e objetivo. Use linguagem natural e clara.
- Integre naturalmente o tópico principal (palavra-chave) sem repetir excessivamente.
- Evite usar listas extensas; prefira parágrafos explicativos.

TRANSCRIÇÃO:
{transcript}

TÍTULO SUGERIDO (ou use o título fornecido se houver): {title}

ARTIGO COM META DESCRIPTION:
"""

# default config
DEFAULT_GENERATION_CONFIG = {
    "temperature": 0.7,
    "max_tokens": 1000,
    "top_p": 0.9,
}