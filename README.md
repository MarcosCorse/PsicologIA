---
title: PsicologIA
emoji: 🧠
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: "1.60.0"
app_file: app.py
pinned: false
license: mit
---

# PsicologIA 🧠

**Analisador Ético de Publicações em Psicologia**

Ferramenta gratuita e open source que analisa publicações de profissionais da Psicologia em redes sociais, identificando possíveis incompatibilidades com:
- Código de Ética Profissional da Psicologia (Resolução CFP nº 010/2005)
- Resoluções complementares do CFP
- Notas técnicas oficiais

## Como funciona

1. Cole o texto da publicação (post, comentário, legenda, transcrição)
2. A IA analisa o conteúdo comparando com as normas do CFP
3. Para cada possível problema, a ferramenta destaca:
   - O trecho exato analisado
   - Explicação em linguagem simples
   - Artigo, alínea ou seção da norma relacionada
   - A relação entre a publicação e a norma
4. Orienta sobre como preservar evidências e contatar o CRP responsável

## Importante

⚠️ **Esta ferramenta NÃO determina que houve infração ética.** Essa decisão cabe exclusivamente aos Conselhos Regionais de Psicologia, após processo ético-disciplinar com direito ao contraditório e ampla defesa.

## Tecnologia

- **Modelo de IA:** Qwen 2.5 7B Instruct (open source, Apache 2.0)
- **Inferência:** Hugging Face Inference API (serverless, gratuito)
- **Interface:** Streamlit
- **Hospedagem:** Hugging Face Spaces

## Privacidade

Nenhuma publicação analisada é armazenada. O texto é enviado apenas para a API de inferência do Hugging Face durante a análise e não é retido.

## Configuração

Para rodar este Space, é necessário configurar um token do Hugging Face:

1. Crie uma conta em [huggingface.co](https://huggingface.co)
2. Gere um token em [Settings > Access Tokens](https://huggingface.co/settings/tokens)
3. No Space, vá em **Settings > Repository secrets**
4. Adicione: `HF_TOKEN` = `hf_seu_token_aqui`

## Base de dados

A ferramenta inclui:
- Contatos dos 23 Conselhos Regionais de Psicologia + Conselho Federal
- Orientações sobre como preservar evidências e formalizar denúncias
