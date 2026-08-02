import json
import os
from huggingface_hub import InferenceClient

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

MODELOS_HF = {
    "Qwen 2.5 7B (Recomendado)": "Qwen/Qwen2.5-7B-Instruct",
    "Mistral 7B (França)": "mistralai/Mistral-7B-Instruct-v0.3",
    "Llama 3.1 8B": "meta-llama/Meta-Llama-3.1-8B-Instruct",
}

MODELO_PADRAO = "Qwen/Qwen2.5-7B-Instruct"


def _obter_token():
    token = os.environ.get("HF_TOKEN", "")
    if not token:
        try:
            import streamlit as st
            token = st.secrets.get("HF_TOKEN", "")
        except Exception:
            pass
    return token


def _carregar_artigos():
    caminho = os.path.join(DATA_DIR, "codigo_etica.json")
    with open(caminho, "r", encoding="utf-8") as f:
        dados = json.load(f)

    linhas = [f"# {dados['documento']} ({dados['norma']})\n"]

    for princ in dados.get("principios_fundamentais", []):
        linhas.append(princ)

    linhas.append("")

    for artigo in dados["artigos"]:
        linhas.append(f"## {artigo['id']} — {artigo['tipo']}")
        for item in artigo["itens"]:
            linhas.append(f"- {item['letra']}) {item['texto']}")
        linhas.append("")

    return "\n".join(linhas)


def _carregar_resolucoes():
    caminho = os.path.join(DATA_DIR, "resolucoes.json")
    with open(caminho, "r", encoding="utf-8") as f:
        dados = json.load(f)

    linhas = [f"# {dados['documento']}\n"]
    for res in dados["resolucoes"]:
        linhas.append(f"## {res['id']}: {res['titulo']}")
        for ponto in res["pontos_relevantes"]:
            linhas.append(f"- {ponto}")
        linhas.append("")

    return "\n".join(linhas)


def _construir_prompt(texto_publicacao):
    artigos = _carregar_artigos()
    resolucoes = _carregar_resolucoes()

    prompt = f"""Você é um assistente especializado em ética profissional da Psicologia no Brasil.
Sua função é analisar publicações feitas por profissionais da Psicologia em redes sociais
e identificar possíveis incompatibilidades com as normas do Conselho Federal de Psicologia (CFP).

**REGRAS FUNDAMENTAIS:**
1. NUNCA afirme categoricamente que houve infração ética. Use linguagem como
   "pode estar em desacordo com", "apresenta possível incompatibilidade com",
   "há indícios de desrespeito a", "o trecho sugere conflito com".
2. Explique SEMPRE em linguagem simples e acessível, como se estivesse falando
   com uma pessoa que não é da área jurídica.
3. Para cada possível problema, cite EXATAMENTE qual artigo, alínea e/ou seção
   da norma oficial está relacionado.
4. Explique de forma clara a RELAÇÃO entre o trecho da publicação e a norma citada.
5. Se houver múltiplos problemas, analise CADA UM separadamente.
6. Se não encontrar nenhum problema, diga que não foram identificadas
   incompatibilidades relevantes com base nas normas disponíveis.
7. NÃO invente artigos ou normas que não estejam na lista fornecida abaixo.
8. Sua análise deve ser técnica, objetiva e impessoal.

---

**NORMAS DE REFERÊNCIA:**

{artigos}

{resolucoes}

---

**PUBLICAÇÃO A SER ANALISADA:**

"{texto_publicacao}"

---

Responda no seguinte formato estruturado:

## RESUMO GERAL
[Um parágrafo curto resumindo a análise como um todo]

## ANÁLISE DETALHADA

### Possível problema 1: [Título descritivo curto]

**Trecho analisado:**
> [Cópia exata do trecho da publicação]

**O que pode estar inadequado (em linguagem simples):**
[Explicação clara, sem juridiquês]

**Norma relacionada:**
[Nome do documento] — [Artigo, alínea ou seção]

**Texto da norma:**
> [Transcrição literal do artigo/alínea]

**Relação entre a publicação e a norma:**
[Explicação conectando o trecho com a norma]

---

[Repetir para cada possível problema]

---

## ORIENTAÇÕES
[Se aplicável, orientar sobre como proceder: preservar evidências, procurar
o Conselho Regional, etc. Lembre-se de incluir a ressalva de que apenas o CRP
pode decidir se houve infração após processo ético.]
"""
    return prompt


def analisar_publicacao(texto_publicacao, modelo=None):
    if modelo is None:
        modelo = MODELO_PADRAO

    token = _obter_token()
    if not token:
        raise RuntimeError(
            "Token do Hugging Face não encontrado. Configure a variável HF_TOKEN "
            "ou adicione em .streamlit/secrets.toml: HF_TOKEN = 'hf_...'"
        )

    client = InferenceClient(token=token, model=modelo)
    prompt = _construir_prompt(texto_publicacao)

    resposta = client.chat_completion(
        messages=[
            {
                "role": "system",
                "content": (
                    "Você é um assistente de análise ética profissional. "
                    "Responda sempre em português brasileiro, em formato markdown. "
                    "Seja objetivo, técnico e impessoal."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=4096,
        temperature=0.3,
    )

    return resposta.choices[0].message.content


def extrair_texto_imagem(imagem_bytes, modelo_ocr=None):
    """Extrai texto de uma imagem usando OCR via Hugging Face."""
    if modelo_ocr is None:
        modelo_ocr = "microsoft/trocr-base-printed"

    token = _obter_token()
    if not token:
        raise RuntimeError("Token do Hugging Face não configurado.")

    client = InferenceClient(token=token, model=modelo_ocr)
    resultado = client.image_to_text(imagem_bytes)
    return resultado


def listar_modelos_disponiveis():
    return MODELOS_HF
