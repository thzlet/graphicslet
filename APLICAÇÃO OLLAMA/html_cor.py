def gerar_html(dados: dict, caminho_saida: str = "cor_gerada.html") -> str:
    r = dados["r"]
    g = dados["g"]
    b = dados["b"]

    nome = dados.get("cor_nome", "cor")
    hex_cor = f"#{r:02X}{g:02X}{b:02X}"

    html = f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<title>Cor extraída: {nome}</title>

<style>
    body {{
        font-family: sans-serif;
        background: #111;
        color: #eee;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh;
    }}

    .quadrado {{
        width: 200px;
        height: 200px;
        background: {hex_cor};
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,.5);
    }}

    p {{
        font-family: monospace;
        margin-top: 16px;
    }}
</style>
</head>

<body>
    <div class="quadrado"></div>

    <p>
        {nome} |
        RGB({r}, {g}, {b}) |
        {hex_cor}
    </p>
</body>
</html>
"""

    with open(caminho_saida, "w", encoding="utf-8") as arquivo:
        arquivo.write(html)

    return caminho_saida
