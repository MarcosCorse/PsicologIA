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
    /* Fundo geral */
    .stApp {
        background-color: #f8faff;
    }

    /* Botão primário */
    .stButton > button {
        background: linear-gradient(135deg, #1e6fbf 0%, #2d8ad4 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #1a5a9e 0%, #2578b8 100%);
        box-shadow: 0 2px 8px rgba(30, 111, 191, 0.3);
    }

    /* Botão secundário */
    .stButton > button[kind="secondary"] {
        background: white;
        color: #1e6fbf;
        border: 1.5px solid #1e6fbf;
    }
    .stButton > button[kind="secondary"]:hover {
        background: #e8f0fa;
    }

    /* Cards e containers */
    .stExpander {
        background: white;
        border: 1px solid #d8e4f0;
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #4a6a8a;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        color: #1e6fbf;
        font-weight: 600;
        border-bottom: 2px solid #1e6fbf;
    }

    /* Área de texto */
    .stTextArea textarea {
        border: 1.5px solid #c8d8e8;
        border-radius: 8px;
        background: white;
    }
    .stTextArea textarea:focus {
        border-color: #1e6fbf;
        box-shadow: 0 0 0 2px rgba(30, 111, 191, 0.1);
    }

    /* Select e file uploader */
    .stSelectbox > div > div {
        border-radius: 8px;
    }
    .stFileUploader {
        background: #f0f5fb;
        border: 1.5px dashed #a8c4e0;
        border-radius: 10px;
        padding: 1rem;
    }

    /* Alertas coloridos */
    .stSuccess { background-color: #e8f5e9; border-left: 4px solid #2e7d32; }
    .stWarning { background-color: #fff8e1; border-left: 4px solid #f9a825; }
    .stError   { background-color: #ffebee; border-left: 4px solid #c62828; }
    .stInfo    { background-color: #e3f2fd; border-left: 4px solid #1e6fbf; }

    /* Rodapé */
    .footer {
        text-align: center;
        color: #7a8ea0;
        font-size: 0.8rem;
        padding: 1.5rem 0 0.5rem 0;
        border-top: 1px solid #d8e4f0;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Header customizado
col_logo, _ = st.columns([1, 3])
with col_logo:
    st.image("assets/logo.png", use_container_width=True)

st.divider()

st.markdown(
    '<p style="font-size: 16px; color: #3a4a5a; line-height: 1.6; text-align: justify;">'
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
    <a href="https://github.com/MarcosCorse/PsicologIA" style="color: #1e6fbf;">GitHub</a>
    <br>Esta ferramenta não substitui denúncia formal ao Conselho Regional de Psicologia.
</div>
""", unsafe_allow_html=True)
