import streamlit as st
from src.analisador import analisar_publicacao, listar_modelos_disponiveis
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

    with col1:
        texto = st.text_area(
            "Cole aqui a publicação, comentário, legenda ou transcrição:",
            height=250,
            placeholder=(
                "Exemplo:\n"
                '"Sou psicóloga há 15 anos. Prometo resultado em 3 sessões para '
                'qualquer tipo de ansiedade. Me chame no direct para agendar!"\n\n'
                "— Você pode colar textos longos. A IA analisará trecho por trecho."
            ),
        )

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
        - Não analisa imagens (apenas texto)

        **Tecnologia:**
        - IA: Qwen 2.5 7B (open source, Apache 2.0)
        - Hospedagem: Hugging Face Spaces
        - 100% open source, sem big techs
        """
        )

        modelos = listar_modelos_disponiveis()
        nome_modelo = st.selectbox(
            "Modelo de IA:",
            list(modelos.keys()),
            index=0,
            help="Qwen 2.5 é o mais equilibrado em qualidade e velocidade para português.",
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
                    if "token" in erro.lower() or "HF_TOKEN" in erro:
                        st.error(
                            "❌ Token do Hugging Face não configurado. "
                            "Configure a variável de ambiente HF_TOKEN ou adicione "
                            "nos Secrets do Space: `HF_TOKEN = 'hf_...'`"
                        )
                    elif "429" in erro or "rate" in erro.lower():
                        st.error(
                            "❌ Limite de requisições excedido. Aguarde alguns segundos e tente novamente."
                        )
                    elif "auth" in erro.lower() or "401" in erro:
                        st.error(
                            "❌ Token inválido. Verifique seu HF_TOKEN."
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
