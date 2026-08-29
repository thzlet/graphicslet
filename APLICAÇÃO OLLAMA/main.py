import sys
import webbrowser

from ollama_cor import extrair_rgb
from html_cor import gerar_html


def main():
    if len(sys.argv) > 1:
        texto = " ".join(sys.argv[1:])
    else:
        texto = input(
            "Descreva a cor (ex.: 'bola rosa'): "
        )

    try:
        dados = extrair_rgb(texto)

        print("Cor extraída:", dados)

        caminho = gerar_html(dados)

        print(f"Arquivo gerado: {caminho}")

        webbrowser.open(caminho)

    except Exception as erro:
        print(f"Erro: {erro}")


if __name__ == "__main__":
    main()
