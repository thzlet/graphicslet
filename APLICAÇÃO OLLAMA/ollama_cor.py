import json
import re
import ollama

MODEL_NAME = "llama3.2"

SYSTEM_PROMPT = (
    "Você é um assistente que extrai a cor principal mencionada em uma frase "
    "e converte para um código RGB (0-255). "
    "Responda ESTRITAMENTE em JSON, sem nenhum texto adicional, no formato: "
    '{"cor_nome": "<nome da cor em portugues>", "r": <int 0-255>, '
    '"g": <int 0-255>, "b": <int 0-255>}'
)

def extrair_rgb(texto: str) -> dict:
    resposta = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": texto},
        ],
    )

    conteudo = resposta["message"]["content"].strip()

    match = re.search(r"\{.*\}", conteudo, re.DOTALL)

    if not match:
        raise ValueError(
            f"Não consegui extrair um JSON válido da resposta:\n{conteudo}"
        )

    dados = json.loads(match.group(0))

    for chave in ("r", "g", "b"):
        dados[chave] = max(0, min(255, int(dados[chave])))

    return dados
