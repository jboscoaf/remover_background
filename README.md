# Removedor de Fundo de Imagens com IA

Este é um projeto desenvolvido em Python que utiliza Inteligência Artificial para remover o fundo de qualquer imagem automaticamente, gerando um arquivo transparente no formato `.png`.

## Tecnologias Utilizadas
* **Python**
* **Streamlit** (Interface Web)
* **Hugging Face Transformers** (Pipeline de IA)
* **BriaAI RMBG-1.4** (Modelo de Segmentação de Imagem leve e eficiente)

## Como rodar o projeto localmente

1. Criar um ambiente virtual:
   ```bash
   python -m venv .venv
   ```
2. Ativar o ambiente virtual:
   * Windows: `.\.venv\Scripts\activate`
   * Linux/Mac: `source .venv/bin/activate`
3. Instalar as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Executar o aplicativo:
   ```bash
   streamlit run app.py
   ```
