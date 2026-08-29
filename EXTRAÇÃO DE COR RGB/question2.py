import json
import re
import sys
import webbrowser
import ollama

MODEL_NAME = "llama3.2"  # troque pelo modelo que você tiver baixado no Ollama

SYSTEM_PROMPT = (
    "Você é um assistente que extrai a cor principal mencionada em uma frase "
    "e converte para um código RGB (0-255). "
    "Responda ESTRITAMENTE em JSON, sem nenhum texto adicional, no formato: "
    '{"cor_nome": "<nome da cor em portugues>", "r": <int 0-255>, "g": <int 0-255>, "b": <int 0-255>}'
)


def extrair_rgb(texto: str) -> dict:
    """Chama o modelo local via Ollama e retorna um dict {cor_nome, r, g, b}."""
    resposta = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": texto},
        ],
    )

    conteudo = resposta["message"]["content"].strip()

    # Fallback: caso o modelo retorne algum texto extra em volta do JSON,
    # extrai apenas o trecho entre chaves.
    match = re.search(r"\{.*\}", conteudo, re.DOTALL)
    if not match:
        raise ValueError(f"Não consegui extrair um JSON válido da resposta:\n{conteudo}")

    dados = json.loads(match.group(0))

    # validação básica
    for chave in ("r", "g", "b"):
        dados[chave] = max(0, min(255, int(dados[chave])))

    return dados


def gerar_html(dados: dict, caminho_saida: str = "cor_gerada.html") -> str:
    r, g, b = dados["r"], dados["g"], dados["b"]
    nome = dados.get("cor_nome", "cor")
    hex_cor = f"#{r:02X}{g:02X}{b:02X}"

    html = f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<title>Cor extraída: {nome}</title>
<style>
  body {{ font-family: sans-serif; background:#111; color:#eee; display:flex;
          flex-direction:column; align-items:center; justify-content:center; height:100vh; }}
  .quadrado {{ width:200px; height:200px; background:{hex_cor}; border-radius:12px;
               box-shadow:0 4px 20px rgba(0,0,0,.5); }}
  p {{ font-family: monospace; margin-top: 16px; }}
</style>
</head>
<body>
  <div class="quadrado"></div>
  <p>{nome} &nbsp;|&nbsp; RGB({r}, {g}, {b}) &nbsp;|&nbsp; {hex_cor}</p>
</body>
</html>
"""
    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.write(html)

    return caminho_saida


def main():
    texto = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Descreva a cor (ex.: 'bola vermelha'): ")

    dados = extrair_rgb(texto)
    print("Cor extraída:", dados)

    caminho = gerar_html(dados)
    print(f"Arquivo gerado: {caminho}")

    try:
        webbrowser.open(caminho)
    except Exception:
        pass


if __name__ == "__main__":
    main()