"""
Configurações de prompts para o serviço de LLM
"""

SUMMARY_PROMPT_TEMPLATE = """Você é um assistente especializado em criar resumos estruturados de vídeos do YouTube.

Analise a seguinte transcrição de vídeo e crie um resumo estruturado seguindo EXATAMENTE este formato:

**INTRODUÇÃO** (2-3 linhas resumindo o tema principal do vídeo)

**PONTOS PRINCIPAIS**
• Ponto 1: [descrição clara e concisa]
• Ponto 2: [descrição clara e concisa]
• Ponto 3: [descrição clara e concisa]
• Ponto 4: [descrição clara e concisa]
• Ponto 5: [descrição clara e concisa]

**CONCLUSÃO** (2-3 linhas com as principais takeaways)

---

TRANSCRIÇÃO DO VÍDEO:
{transcript}

---

RESUMO ESTRUTURADO:"""

TOPICS_PROMPT_TEMPLATE = """Você é um assistente especializado em extrair os principais tópicos abordados em vídeos do YouTube.

Analise a seguinte transcrição e identifique os 3-5 tópicos/temas MAIS IMPORTANTES discutidos no vídeo.

Para cada tópico, forneça:
1. Nome do tópico (curto e direto)
2. Breve descrição (1 linha explicando o que foi discutido)

Formato de saída (siga EXATAMENTE):
• **Tópico 1**: Descrição breve
• **Tópico 2**: Descrição breve
• **Tópico 3**: Descrição breve

---

TRANSCRIÇÃO DO VÍDEO:
{transcript}

---

TÓPICOS PRINCIPAIS:"""

# default config
DEFAULT_GENERATION_CONFIG = {
    "temperature": 0.7,
    "max_tokens": 1000,
    "top_p": 0.9,
}