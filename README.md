# 📊 OSRS Wiki Stats

Este é um projeto em Python que acessa a **Old School RuneScape Wiki (OSRS Wiki)** via API para coletar estatísticas sobre o site, como o número total de artigos.

## 🚀 Funcionalidades

- Consulta a API oficial da OSRS Wiki (`api.php`).
- Obtém estatísticas do site (ex.: total de artigos).
- Mostra o resultado no terminal.
- Usa um **User-Agent customizado** para respeitar as regras de acesso da Wiki.

## 📦 Requisitos

- Python 3.8 ou superior
- Dependências (instale com `pip`):

```bash
pip install requests
```

## Como executar

Clone o repositório ou baixe o arquivo e rode:

```bash
python3 teste.py
```

Saída esperada (exemplo):

```bash
Número total de artigos na OSRS Wiki: 246,789
```

## ⚠️ Importante sobre o uso da API

A OSRS Wiki é hospedada pela Weird Gloop e utiliza MediaWiki API.
Para evitar bloqueio do servidor:

Sempre use um User-Agent descritivo no seu script, incluindo:

- Nome do projeto
- Versão
- Forma de contato (e-mail ou link para GitHub/site)

Exemplo no código:
```bash
headers = {
    "User-Agent": "OSRSWikiStatsBot/0.1 (https://github.com/seuusuario ou email@dominio.com)"
}
```
- Não faça requisições em excesso (respeite limites de taxa, insira time.sleep() se necessário).
- Confira a documentação oficial da API:
    - MediaWiki API
    - Sandbox da OSRS Wiki

## 🔮 Próximos passos (idéias)

- Salvar as estatísticas em um arquivo CSV para acompanhar evolução ao longo do tempo.
- Coletar links entre artigos e montar grafos interativos (ex.: usando networkx + pyvis).
- Criar dashboards com visualização de dados (Plotly, Dash, etc.).

## 📜 Licença

Este projeto é apenas para fins de aprendizado/estudo. Respeite sempre as regras de uso da OSRS Wiki e não abuse da API.