import streamlit as st
from src.analisador import analisar_publicacao, extrair_texto_imagem, listar_modelos_disponiveis
from src.crp_manager import (
    buscar_crp_por_estado,
    obter_orientacao_denuncia,
    obter_info_cfp,
    MAPA_ESTADOS,
)

st.set_page_config(
    page_title="PsicologIA — Análise Ética de Publicações",
    page_icon="🧠",
    layout="wide",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&display=swap');

    html, body, .stMarkdown, .stText, p, label, button, input, textarea, select, h1, h2, h3, h4, h5, h6 {
        font-family: 'Sora', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Fundo azul */
    .stApp {
        background: #009DCF;
    }

    /* Cartão principal flutuante */
    .main .block-container {
        background: rgba(255, 255, 255, 0.75);
        border-radius: 20px;
        padding: 2rem 2.5rem;
        margin: 1.2rem 1rem;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #c0dff2;
    }
    [data-testid="stSidebar"] .block-container {
        padding: 1.5rem 1rem;
    }

    /* Botão primário */
    .stButton > button {
        background: #007aad;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.65rem 1.8rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.2s;
        box-shadow: 0 2px 8px rgba(0, 90, 130, 0.2);
    }
    .stButton > button:hover {
        background: #006a98;
        box-shadow: 0 4px 16px rgba(0, 90, 130, 0.3);
        transform: translateY(-1px);
    }

    .stButton > button[kind="secondary"] {
        background: white;
        color: #007aad;
        border: 1.5px solid #b8d8e8;
        box-shadow: none;
    }
    .stButton > button[kind="secondary"]:hover {
        background: #eef6fa;
        border-color: #007aad;
    }

    /* Textarea */
    .stTextArea textarea {
        border: 1.5px solid #c5dded;
        border-radius: 14px;
        background: #f6fafd;
        font-size: 15px;
        padding: 14px 18px;
        color: #1a202c;
    }
    .stTextArea textarea:focus {
        border-color: #009DCF;
        box-shadow: 0 0 0 3px rgba(0, 157, 207, 0.1);
    }

    /* Upload */
    .stFileUploader {
        border: 2px dashed #c0d6e4;
        border-radius: 14px;
        padding: 1rem;
    }
    .stFileUploader:hover {
        border-color: #009DCF;
        background: #f4f9fc;
    }

    /* Expanders */
    .stExpander {
        border: 1px solid #edf2f7;
        border-radius: 14px;
        background: white;
    }

    /* Alertas */
    .stWarning {
        background: #fef9f0;
        border-left: 4px solid #e8a030;
        border-radius: 12px;
    }

    /* Rodapé */
    .footer {
        text-align: center;
        color: #7a8fa0;
        font-size: 0.85rem;
        padding: 2rem 0 0.8rem 0;
        border-top: 1px solid #e8eef4;
        margin-top: 2.5rem;
    }
    .footer a {
        color: #007aad;
    }

    /* Select */
    .stSelectbox > div > div {
        border-radius: 10px;
    }

    /* ── Cards ── */
    .card {
        background: #d0e8f5;
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.2rem;
        border: 2px solid #009DCF;
        box-shadow: 0 4px 16px rgba(0, 60, 100, 0.1);
    }
    .card-header {
        font-size: 1.1rem;
        font-weight: 700;
        color: #004466;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .card-icon {
        font-size: 1.3rem;
    }

    /* ── Barra de passos ── */
    .steps {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin: 1.5rem 0 2rem 0;
        text-align: center;
    }
    .step {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.3rem;
        opacity: 0.5;
    }
    .step.active { opacity: 1; }
    .step-circle {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: #c5e0f0;
        color: #0d3b5c;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.9rem;
    }
    .step.active .step-circle {
        background: #007aad;
        color: white;
    }
    .step-label {
        font-size: 0.78rem;
        font-weight: 500;
        color: #4a7a9a;
    }
    .step.active .step-label {
        color: #0d3b5c;
        font-weight: 600;
    }
    .step-line {
        width: 60px;
        height: 2px;
        background: #c5e0f0;
        margin-top: 17px;
    }

    /* ── Badges ── */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.7rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.02em;
    }
    .badge-blue   { background: #e0f0f8; color: #007aad; }
    .badge-green  { background: #e6f4ea; color: #1e7e34; }
    .badge-amber  { background: #fef3e0; color: #b45309; }

    /* ── Banner decorativo ── */
    .banner {
        background: linear-gradient(135deg, #007aad 0%, #009DCF 40%, #4db8e0 100%);
        border-radius: 20px;
        padding: 2rem 2.5rem;
        margin-bottom: 1.5rem;
        color: white;
        position: relative;
        overflow: hidden;
    }
    .banner::before {
        content: '';
        position: absolute;
        top: -60px;
        right: -40px;
        width: 200px;
        height: 200px;
        background: rgba(255,255,255,0.08);
        border-radius: 50%;
    }
    .banner::after {
        content: '';
        position: absolute;
        bottom: -80px;
        left: 20%;
        width: 250px;
        height: 250px;
        background: rgba(255,255,255,0.05);
        border-radius: 50%;
    }
    .banner-text {
        position: relative;
        z-index: 1;
        font-size: 1rem;
        line-height: 1.7;
        font-weight: 400;
    }
</style>
""", unsafe_allow_html=True)

# Header customizado
col_logo, _ = st.columns([1, 1])
with col_logo:
    st.image("assets/logo.png", use_container_width=True)

st.caption("v2.0 — Cards · Banner · Passos · Badges")

st.divider()

# ── Banner decorativo ─────────────────────────────────────────

st.markdown("""
<div class="banner">
    <p class="banner-text">
        Está pesquisando um psicólogo ou uma psicóloga e quer entender melhor
        as informações apresentadas no perfil profissional? O <strong>PsicologIA</strong>
        ajuda você a analisar dados como identificação, registro profissional, formação,
        títulos, serviços oferecidos e formas de divulgação, sinalizando pontos que podem
        estar em desacordo com as normas da Psicologia.
        <br><br>
        <span class="badge badge-blue">Gratuito</span>
        <span class="badge badge-green">Open Source</span>
        <span class="badge badge-amber">IA · DeepSeek</span>
    </p>
</div>
""", unsafe_allow_html=True)

# ── Barra de passos ───────────────────────────────────────────

st.markdown("""
<div class="steps">
    <div class="step active">
        <div class="step-circle">1</div>
        <div class="step-label">Cole o texto</div>
    </div>
    <div class="step-line"></div>
    <div class="step">
        <div class="step-circle">2</div>
        <div class="step-label">Confirme</div>
    </div>
    <div class="step-line"></div>
    <div class="step">
        <div class="step-circle">3</div>
        <div class="step-label">Resultado</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────

with st.sidebar:
    st.markdown(
        '<h3 style="color: #1a3a5c;">Ψ Encontre o Conselho Regional de Psicologia</h3>',
        unsafe_allow_html=True,
    )

    ufs = [""] + sorted(MAPA_ESTADOS.keys())
    uf_selecionada = st.selectbox(
        "Estado onde o profissional atua:",
        ufs,
        format_func=lambda u: f"{u} — {MAPA_ESTADOS[u]}" if u else "Selecione...",
    )

    if uf_selecionada:
        crp = buscar_crp_por_estado(uf_selecionada)
        if crp:
            st.success(f"**{crp['sigla']}** — {crp['nome']}")
            st.markdown(f"📧 {crp['email']}")
            st.markdown(f"📞 {crp['telefone']}")
            st.markdown(f"🌐 [{crp['site']}]({crp['site']})")
            if crp.get("observacao"):
                st.info(crp["observacao"])
        else:
            st.warning("Estado não encontrado.")

    cfp = obter_info_cfp()
    with st.expander(f"📋 {cfp['sigla']} — Conselho Federal"):
        st.caption(f"📧 {cfp['email']}")
        st.caption(f"📞 {cfp['telefone']}")
        st.caption(f"🌐 [{cfp['site']}]({cfp['site']})")

    st.markdown("---")

    st.caption(
        "⚠️ Esta ferramenta NÃO determina infração ética. "
        "Apenas o CRP pode decidir após processo formal."
    )

    st.markdown("---")

    with st.expander("⚙️ Configuração"):
        modelos = listar_modelos_disponiveis()
        nome_modelo = st.selectbox(
            "Modelo de IA:",
            list(modelos.keys()),
            index=0,
        )
        modelo_id = modelos[nome_modelo]

# ── Área principal ───────────────────────────────────────────

# Card 1: Entrada
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-header"><span class="card-icon">📝</span> Envie a publicação para análise</div>', unsafe_allow_html=True)

# Estado para texto extraído de imagem
if "texto_ocr" not in st.session_state:
    st.session_state.texto_ocr = ""

texto_padrao = st.session_state.texto_ocr or ""
texto = st.text_area(
    "Cole aqui a publicação, comentário, legenda ou transcrição:",
    value=texto_padrao,
    height=180,
    placeholder=(
        "Exemplo:\n"
        '"Sou psicóloga há 15 anos. Prometo resultado em 3 sessões para '
        'qualquer tipo de ansiedade. Me chame no direct para agendar!"'
    ),
)

imagem = st.file_uploader(
    "Ou envie um print de rede social (PNG, JPG):",
    type=["png", "jpg", "jpeg"],
)

if imagem is not None:
    col_img, col_btn = st.columns([3, 2])
    with col_img:
        st.image(imagem, caption="Prévia", use_container_width=True)
    with col_btn:
        if st.button("📷 Extrair texto da imagem", use_container_width=True):
            with st.spinner("Lendo texto da imagem..."):
                try:
                    texto_extraido = extrair_texto_imagem(imagem.getvalue())
                    st.session_state.texto_ocr = texto_extraido
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro no OCR: {e}")

    if st.session_state.texto_ocr:
        st.caption("✅ Texto extraído. Confira e edite no campo acima antes de analisar.")
        if st.button("🗑️ Limpar texto extraído"):
            st.session_state.texto_ocr = ""
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Card 2: Confirmação e análise
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-header"><span class="card-icon">⚖️</span> Confirme e analise</div>', unsafe_allow_html=True)

st.warning(
    "⚠️ A ferramenta sinaliza possíveis incompatibilidades com as normas "
    "do Conselho Federal de Psicologia (CFP), mas **não determina se houve "
    "infração ética**. Essa avaliação e a decisão final cabem exclusivamente "
    "aos Conselhos Regionais de Psicologia."
)

confirmou = st.checkbox(
    "Declaro que entendi: esta ferramenta não determina infração ética.",
    value=False,
)

if st.button(
    "🔍 Analisar Publicação",
    type="primary",
    use_container_width=True,
    disabled=not confirmou,
):
    if not texto.strip():
        st.warning("Por favor, cole o texto da publicação antes de analisar.")
    else:
        with st.spinner("Analisando com IA... Isso pode levar alguns segundos."):
            try:
                resultado = analisar_publicacao(texto, modelo_id)
                st.success("✅ Análise concluída!")
                st.markdown("---")
                st.markdown(resultado)
            except Exception as e:
                erro = str(e)
                if "DEEPSEEK" in erro.upper() or "api_key" in erro.lower():
                    st.error("❌ Chave da DeepSeek não configurada. Adicione nos Secrets do Streamlit Cloud.")
                elif "429" in erro or "rate" in erro.lower():
                    st.error("❌ Limite de requisições excedido. Aguarde e tente novamente.")
                elif "auth" in erro.lower() or "401" in erro:
                    st.error("❌ Chave da DeepSeek inválida.")
                elif "402" in erro or "saldo" in erro.lower() or "balance" in erro.lower():
                    st.error("❌ Saldo insuficiente na DeepSeek.")
                else:
                    st.error(f"❌ Erro durante a análise: {erro}")

st.markdown('</div>', unsafe_allow_html=True)

# Card 3: Orientações
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-header"><span class="card-icon">📋</span> Como preservar evidências e denunciar</div>', unsafe_allow_html=True)

with st.expander("Clique para ver o passo a passo"):
    orientacao = obter_orientacao_denuncia()
    st.info(orientacao["introducao"])
    for passo in orientacao["passos"]:
        st.markdown(f"**{passo['passo']}. {passo['titulo']}**  \n{passo['descricao']}")
    st.warning(orientacao["ressalva_final"])

st.markdown('</div>', unsafe_allow_html=True)

# Rodapé
st.markdown("""
<div class="footer">
    PsicologIA · v1.0 · Tecnologia DeepSeek (China) · Open source · 
    <a href="https://github.com/MarcosCorse/PsicologIA">GitHub</a>
    <br>Esta ferramenta não substitui denúncia formal ao Conselho Regional de Psicologia.
</div>
""", unsafe_allow_html=True)
