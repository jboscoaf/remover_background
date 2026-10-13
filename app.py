import streamlit as st
from transformers import pipeline
from PIL import Image
from io import BytesIO

# Configuração da página da web
st.set_page_config(page_title="Remover Fundo IA", page_icon="✂️", layout="centered")

st.title("✂️ Remoção de Background Automática")
st.write("Envie uma imagem e escolha se deseja o fundo transparente ou com uma cor personalizada.")

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

# --- NOVO BLOCO: SELEÇÃO DE COR DE FUNDO ---
st.sidebar.header("🎨 Configurações de Fundo")
tipo_fundo = st.sidebar.radio("Escolha o tipo de fundo:", ["Transparente (PNG)", "Cor Sólida"])

cor_fundo = "#FFFFFF" # Padrão branco caso escolha cor sólida
if tipo_fundo == "Cor Sólida":
    cor_fundo = st.sidebar.color_picker("Escolha a cor do fundo:", "#3B82F6") # Azul padrão inicial
# --------------------------------------------

# Componente de upload de imagem na tela
arquivo_enviado = st.file_uploader("Escolha uma imagem do seu computador...", type=["jpg", "jpeg", "png"])

if arquivo_enviado is not None:
    imagem_input = Image.open(arquivo_enviado).convert("RGBA") # Garante formato RGBA para trabalhar com transparência
    
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
                # 1. A IA remove o fundo original e gera uma imagem transparente
                imagem_transparente = remover_fundo(imagem_input).convert("RGBA")
                
                # 2. Se o usuário escolheu Cor Sólida, criamos um fundo colorido e colamos a imagem por cima
                if tipo_fundo == "Cor Sólida":
                    # Cria uma imagem sólida do mesmo tamanho da imagem original com a cor escolhida
                    fundo_colorido = Image.new("RGBA", imagem_transparente.size, cor_fundo)
                    # Mescla a imagem sem fundo por cima do fundo colorido
                    imagem_resultado = Image.alpha_composite(fundo_colorido, imagem_transparente)
                else:
                    imagem_resultado = imagem_transparente
                
                st.image(imagem_resultado, use_container_width=True)
                st.success("Pronto!")
                processado_com_sucesso = True
            except Exception as e:
                st.error(f"Ocorreu um erro no processamento: {e}")

    # O botão aparece centralizado abaixo de tudo
    if processado_com_sucesso and imagem_resultado is not None:
        st.write("---")
        imagem_em_bytes = converter_imagem(imagem_resultado)
        st.download_button(
            label="📥 Clique aqui para Baixar o Resultado (PNG)",
            data=imagem_em_bytes,
            file_name="imagem_processada.png",
            mime="image/png",
            use_container_width=True
        )

