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

st.title("PsicologIA")
st.subheader("Análise Ética de Publicações em Psicologia")
st.caption(
    "Ferramenta gratuita e open source para orientação da sociedade. "
    "Identifica possíveis incompatibilidades com as normas do CFP. "
    "A decisão final sobre infrações éticas cabe exclusivamente aos Conselhos Regionais de Psicologia."
)

tab1, tab2 = st.tabs(["Analisar Publicação", "Buscar Conselho Regional"])

# ── TAB 1: Análise ──────────────────────────────────────────────

with tab1:
    col1, col2 = st.columns([2, 1])

    # Estado para texto extraído de imagem
    if "texto_ocr" not in st.session_state:
        st.session_state.texto_ocr = ""

    with col1:
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
                            erro = str(e)
                            if "429" in erro or "rate" in erro.lower():
                                st.error("Limite de requisições excedido. Aguarde e tente novamente.")
                            elif "not found" in erro.lower():
                                st.error("Modelo de OCR indisponível no momento. Tente novamente mais tarde.")
                            else:
                                st.error(f"Erro no OCR: {e}")


            if st.session_state.texto_ocr:
                st.caption("✅ Texto extraído. Confira e edite no campo acima antes de analisar.")
                if st.button("Limpar texto extraído"):
                    st.session_state.texto_ocr = ""
                    st.rerun()

    with col2:
        st.markdown("### Sobre esta ferramenta")
        st.markdown(
            """
        **O que ela faz:**
        - Analisa publicações de profissionais da Psicologia
        - Compara com o Código de Ética, resoluções e notas técnicas do CFP
        - Destaca trechos com possíveis problemas
        - Explica o que pode estar inadequado em linguagem simples
        - Cita o artigo ou norma aplicável

        **O que ela NÃO faz:**
        - Não afirma que houve infração (isso cabe ao CRP)
        - Não substitui denúncia formal ao Conselho Regional
        - A extração de texto de imagens depende da qualidade do print

        **Tecnologia:**
        - IA: DeepSeek Chat (DeepSeek, China)
        - OCR: pytesseract (offline, português)
        - Hospedagem: Streamlit Cloud
        - Open source, sem big techs americanas
        """
        )

        modelos = listar_modelos_disponiveis()
        nome_modelo = st.selectbox(
            "Modelo de IA:",
            list(modelos.keys()),
            index=0,
            help="DeepSeek Chat é rápido e preciso. DeepSeek R1 pensa mais antes de responder.",
        )
        modelo_id = modelos[nome_modelo]

    if st.button("Analisar Publicação", type="primary", use_container_width=True):
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
                        st.error(
                            "❌ Limite de requisições excedido. Aguarde alguns segundos e tente novamente."
                        )
                    elif "auth" in erro.lower() or "401" in erro:
                        st.error(
                            "❌ Chave da DeepSeek inválida. Verifique seu DEEPSEEK_API_KEY."
                        )
                    elif "402" in erro or "saldo" in erro.lower() or "balance" in erro.lower():
                        st.error(
                            "❌ Saldo insuficiente na DeepSeek. Recarregue em platform.deepseek.com"
                        )
                    else:
                        st.error(f"❌ Erro durante a análise: {erro}")

    st.markdown("---")
    with st.expander("Como preservar evidências e denunciar"):
        orientacao = obter_orientacao_denuncia()
        st.info(orientacao["introducao"])
        for passo in orientacao["passos"]:
            st.markdown(f"**{passo['passo']}. {passo['titulo']}**  \n{passo['descricao']}")
        st.warning(orientacao["ressalva_final"])

# ── TAB 2: Busca de CRP ─────────────────────────────────────────

with tab2:
    st.header("Encontre o Conselho Regional de Psicologia")

    ufs = [""] + sorted(MAPA_ESTADOS.keys())
    uf_selecionada = st.selectbox(
        "Selecione o estado onde o profissional atua ou onde ocorreu o fato:",
        ufs,
        format_func=lambda u: f"{u} — {MAPA_ESTADOS[u]}" if u else "Selecione um estado...",
    )

    if uf_selecionada:
        crp = buscar_crp_por_estado(uf_selecionada)
        if crp:
            st.success(f"**{crp['sigla']}** — {crp['nome']}")
            st.markdown(
                f"""
            | Informação | Detalhe |
            |---|---|
            | **Abrangência** | {crp['abrangencia']} |
            | **Site** | [{crp['site']}]({crp['site']}) |
            | **E-mail** | {crp['email']} |
            | **Telefone** | {crp['telefone']} |
            """
            )
            if crp.get("observacao"):
                st.info(crp["observacao"])
        else:
            st.warning("Estado não encontrado. Verifique a sigla.")

    st.markdown("---")
    cfp = obter_info_cfp()
    with st.expander(f"Sobre o {cfp['sigla']} (Conselho Federal)"):
        st.markdown(
            f"""
        **{cfp['nome']}**

        - **Site:** [{cfp['site']}]({cfp['site']})
        - **E-mail:** {cfp['email']}
        - **Telefone:** {cfp['telefone']}
        - **Endereço:** {cfp['endereco']}

        **Sobre denúncias ao CFP:** {cfp['canais_denuncia']}
        """
        )
