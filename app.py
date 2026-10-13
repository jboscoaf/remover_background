import streamlit as st
from transformers import pipeline
from PIL import Image
from io import BytesIO

# Configuração da página da web
st.set_page_config(page_title="Remover Fundo IA", page_icon="✂️", layout="centered")

st.title("✂️ Remoção de Background Automática")
st.write("Envie uma imagem e a inteligência artificial removerá o fundo para você em formato PNG.")

# Carrega o modelo de IA usando cache para economizar memória do servidor público
@st.cache_resource
def carregar_modelo():
    return pipeline("image-segmentation", model="briaai/RMBG-1.4", trust_remote_code=True)

# Função que processa a imagem
def remover_fundo(imagem_original):
    pipe = carregar_modelo()
    imagem_sem_fundo = pipe(imagem_original)  
    return imagem_sem_fundo

# Função para converter a imagem PIL para bytes
def converter_imagem(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

# Componente de upload de imagem na tela
arquivo_enviado = st.file_uploader("Escolha uma imagem do seu computador...", type=["jpg", "jpeg", "png"])

if arquivo_enviado is not None:
    imagem_input = Image.open(arquivo_enviado)
    
    # Criamos variáveis vazias para guardar o resultado do processamento
    imagem_resultado = None
    processado_com_sucesso = False
    
    # Exibe as imagens lado a lado (Antes e Depois)
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Original")
        st.image(imagem_input, use_container_width=True)
        
    with col2:
        st.subheader("Resultado")
        with st.spinner("A IA está trabalhando..."):
            try:
                imagem_resultado = remover_fundo(imagem_input)
                st.image(imagem_resultado, use_container_width=True)
                st.success("Pronto!")
                processado_com_sucesso = True
            except Exception as e:
                st.error(f"Ocorreu um erro no processamento: {e}")

    # --- NOVO BLOCO FORA DAS COLUNAS ---
    # O botão agora aparece centralizado abaixo de tudo
    if processado_com_sucesso and imagem_resultado is not None:
        st.write("---") # Adiciona uma linha divisória discreta
        imagem_em_bytes = converter_imagem(imagem_resultado)
        st.download_button(
            label="📥 Clique aqui para Baixar a Imagem sem Fundo (PNG)",
            data=imagem_em_bytes,
            file_name="imagem_sem_fundo.png",
            mime="image/png",
            use_container_width=True
        )
