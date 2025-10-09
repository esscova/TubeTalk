"""
Configurações de prompts para o serviço de LLM
"""

SUMMARY_PROMPT_TEMPLATE = """Por favor, leia a transcrição abaixo e escreva um único parágrafo curto (2-4 frases) que apresente de forma clara e concisa sobre o que trata o vídeo. O parágrafo deve ser informativo, em tom neutro, e servir como uma introdução explicativa para leitores que ainda não assistiram ao vídeo.

Transcrição:
{transcript}

Parágrafo introdutório:"""

TOPICS_PROMPT_TEMPLATE = """Você é um assistente especializado em extrair os principais tópicos abordados em vídeos do YouTube.

Analise a seguinte transcrição e identifique os 3-5 tópicos/temas MAIS IMPORTANTES discutidos no vídeo.

Para cada tópico, forneça:
1. Nome do tópico (curto e direto)
2. Breve descrição (1 linha explicando o que foi discutido)

Formato de saída (siga EXATAMENTE):
• Tópico 1: Descrição breve
• Tópico 2: Descrição breve
• Tópico 3: Descrição breve

---

TRANSCRIÇÃO DO VÍDEO:
{transcript}

---

TÓPICOS PRINCIPAIS:"""

ARTICLE_PROMPT_TEMPLATE = """
Act as an expert copywriter specializing in content optimization for SEO. Your task is to take a given YouTube transcript and transform it into a well-structured and engaging article. Your objectives are as follows:

Content Transformation: Begin by thoroughly reading the provided YouTube transcript. Understand the main ideas, key points, and the overall message conveyed.

Sentence Structure: While rephrasing the content, pay careful attention to sentence structure. Ensure that the article flows logically and coherently.

Keyword Identification: Identify the main keyword or phrase from the transcript. It's crucial to determine the primary topic that the YouTube video discusses.

Keyword Integration: Incorporate the identified keyword naturally throughout the article. Use it in headings, subheadings, and within the body text. However, avoid overuse or keyword stuffing, as this can negatively affect SEO.

Unique Content: Your goal is to make the article 100% unique. Avoid copying sentences directly from the transcript. Rewrite the content in your own words while retaining the original message and meaning.

SEO Friendliness: Craft the article with SEO best practices in mind. This includes optimizing meta tags (title and meta description), using header tags appropriately, and maintaining an appropriate keyword density.

Engaging and Informative: Ensure that the article is engaging and informative for the reader. It should provide value and insight on the topic discussed in the YouTube video.

Proofreading: Proofread the article for grammar, spelling, and punctuation errors. Ensure it is free of any mistakes that could detract from its quality.

By following these guidelines, create a well-optimized, unique, and informative article that would rank well in search engine results and engage readers effectively.

Transcript:{transcript}"""

# default config
DEFAULT_GENERATION_CONFIG = {
    "temperature": 0.7,
    "max_tokens": 1000,
    "top_p": 0.9,
}