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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }

    /* Fundo com formas orgânicas suaves */
    .stApp {
        background:
            radial-gradient(ellipse 80% 60% at 20% 15%, rgba(0, 157, 207, 0.12) 0%, transparent 60%),
            radial-gradient(ellipse 60% 50% at 80% 70%, rgba(100, 180, 220, 0.10) 0%, transparent 55%),
            radial-gradient(circle 40% at 50% 50%, rgba(0, 157, 207, 0.05) 0%, transparent 50%),
            #f8fafc;
        background-attachment: fixed;
    }

    /* Conteúdo principal - card flutuante */
    .main .block-container {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 2rem 2.5rem;
        margin-top: 1rem;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.04), 0 1px 4px rgba(0, 0, 0, 0.03);
        border: 1px solid rgba(0, 0, 0, 0.04);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #fafcfe 100%);
        border-right: 1px solid rgba(0, 0, 0, 0.05);
    }

    /* Botão primário */
    .stButton > button {
        background: linear-gradient(135deg, #007aad 0%, #009DCF 100%);
        color: white;
        border: none;
        border-radius: 14px;
        padding: 0.7rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        letter-spacing: 0.01em;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 12px rgba(0, 157, 207, 0.25);
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #006994 0%, #008bb8 100%);
        box-shadow: 0 6px 20px rgba(0, 157, 207, 0.35);
        transform: translateY(-2px);
    }

    /* Botão secundário */
    .stButton > button[kind="secondary"] {
        background: white;
        color: #007aad;
        border: 2px solid #cde4f0;
        box-shadow: none;
    }
    .stButton > button[kind="secondary"]:hover {
        background: #f0f8fc;
        border-color: #007aad;
    }

    /* Área de texto */
    .stTextArea textarea {
        border: 2px solid #e2e8f0;
        border-radius: 16px;
        background: #fafcfd;
        font-size: 15px;
        padding: 16px 20px;
        transition: all 0.25s;
        color: #1a202c;
    }
    .stTextArea textarea:focus {
        border-color: #009DCF;
        background: white;
        box-shadow: 0 0 0 4px rgba(0, 157, 207, 0.08);
    }

    /* Labels */
    .stTextArea label, .stFileUploader label {
        font-size: 15px;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 0.5rem;
    }

    /* Upload */
    .stFileUploader {
        background: #f8fafc;
        border: 2px dashed #d5e4f0;
        border-radius: 16px;
        padding: 1.5rem;
        transition: all 0.25s;
    }
    .stFileUploader:hover {
        border-color: #009DCF;
        background: #f0f7fb;
        border-style: solid;
    }

    /* Expanders */
    .stExpander {
        background: white;
        border: 1px solid #edf2f7;
        border-radius: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }
    .stExpander > div:first-child {
        font-weight: 600;
        color: #2d3748;
    }

    /* Checkbox */
    .stCheckbox label {
        font-size: 14px;
        color: #4a5568;
        font-weight: 500;
    }

    /* Alertas */
    .stSuccess, .stWarning, .stError, .stInfo {
        border-radius: 14px;
        padding: 1rem 1.3rem;
    }
    .stWarning {
        background-color: #fef7ed;
        border-left: 4px solid #f59e0b;
        border-radius: 14px;
    }

    /* Rodapé */
    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 0.85rem;
        padding: 2.5rem 0 1rem 0;
        border-top: 1px solid #edf2f7;
        margin-top: 3rem;
    }
    .footer a {
        color: #009DCF;
        text-decoration: none;
        font-weight: 500;
    }
    .footer a:hover {
        color: #007aad;
    }

    /* Select */
    .stSelectbox > div > div {
        border-radius: 12px;
    }

    h1, h2, h3, h4 {
        color: #1a202c;
    }
</style>
""", unsafe_allow_html=True)

# Header customizado
col_logo, _ = st.columns([1, 1])
with col_logo:
    st.image("assets/logo.png", use_container_width=True)

st.divider()

st.markdown(
    '<p style="font-size: 18px; color: #0a1f3a; font-weight: 700; line-height: 1.6; text-align: justify; text-shadow: 1px 1px 0px rgba(180, 215, 240, 0.8);">'
    "Está pesquisando um psicólogo ou uma psicóloga e quer entender melhor "
    "as informações apresentadas no perfil profissional? O PsicologIA ajuda você "
    "a analisar dados como identificação, registro profissional, formação, títulos, "
    "serviços oferecidos e formas de divulgação, sinalizando pontos que podem estar "
    "em desacordo com as normas da Psicologia. A ferramenta é gratuita, de código "
    "aberto e foi criada para tornar essa consulta mais simples e acessível, mesmo "
    "para quem não conhece as regras da profissão."
    '</p>',
    unsafe_allow_html=True,
)

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

# Estado para texto extraído de imagem
if "texto_ocr" not in st.session_state:
    st.session_state.texto_ocr = ""

texto_padrao = st.session_state.texto_ocr or ""
texto = st.text_area(
    "Cole aqui a publicação, comentário, legenda ou transcrição:",
    value=texto_padrao,
    height=200,
    placeholder=(
        "Exemplo:\n"
        '"Sou psicóloga há 15 anos. Prometo resultado em 3 sessões para '
        'qualquer tipo de ansiedade. Me chame no direct para agendar!"\n\n'
        "— Você pode colar textos longos ou enviar um print abaixo."
    ),
)

imagem = st.file_uploader(
    "Ou envie um print de rede social (PNG, JPG):",
    type=["png", "jpg", "jpeg"],
    label_visibility="visible",
)

if imagem is not None:
    col_img, col_btn = st.columns([3, 2])
    with col_img:
        st.image(imagem, caption="Prévia", use_container_width=True)
    with col_btn:
        if st.button("Extrair texto da imagem", use_container_width=True):
            with st.spinner("Lendo texto da imagem..."):
                try:
                    texto_extraido = extrair_texto_imagem(imagem.getvalue())
                    st.session_state.texto_ocr = texto_extraido
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro no OCR: {e}")

    if st.session_state.texto_ocr:
        st.caption("✅ Texto extraído. Confira e edite no campo acima antes de analisar.")
        if st.button("Limpar texto extraído"):
            st.session_state.texto_ocr = ""
            st.rerun()

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
                st.success("Análise concluída!")
                st.markdown("---")
                st.markdown(resultado)
            except Exception as e:
                erro = str(e)
                if "DEEPSEEK" in erro.upper() or "api_key" in erro.lower():
                    st.error(
                        "❌ Chave da DeepSeek não configurada. "
                        "Adicione nos Secrets do Streamlit Cloud: "
                        "`DEEPSEEK_API_KEY = 'sk-...'`"
                    )
                elif "429" in erro or "rate" in erro.lower():
                    st.error("❌ Limite de requisições excedido. Aguarde e tente novamente.")
                elif "auth" in erro.lower() or "401" in erro:
                    st.error("❌ Chave da DeepSeek inválida. Verifique seu DEEPSEEK_API_KEY.")
                elif "402" in erro or "saldo" in erro.lower() or "balance" in erro.lower():
                    st.error("❌ Saldo insuficiente na DeepSeek. Recarregue em platform.deepseek.com")
                else:
                    st.error(f"❌ Erro durante a análise: {erro}")

st.markdown("---")
with st.expander("📋 Como preservar evidências e denunciar"):
    orientacao = obter_orientacao_denuncia()
    st.info(orientacao["introducao"])
    for passo in orientacao["passos"]:
        st.markdown(f"**{passo['passo']}. {passo['titulo']}**  \n{passo['descricao']}")
    st.warning(orientacao["ressalva_final"])

# Rodapé
st.markdown("""
<div class="footer">
    PsicologIA · v1.0 · Tecnologia DeepSeek (China) · Open source · 
    <a href="https://github.com/MarcosCorse/PsicologIA">GitHub</a>
    <br>Esta ferramenta não substitui denúncia formal ao Conselho Regional de Psicologia.
</div>
""", unsafe_allow_html=True)
