import json
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def _carregar_json(nome_arquivo):
    caminho = os.path.join(DATA_DIR, nome_arquivo)
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def buscar_crp_por_estado(uf):
    uf = uf.upper().strip()
    dados = _carregar_json("crps.json")

    for regional in dados["regionais"]:
        if uf in regional["estados"]:
            return {
                "sigla": regional["sigla"],
                "nome": regional["nome"],
                "abrangencia": regional["abrangencia"],
                "site": regional["site"],
                "email": regional["email"],
                "telefone": regional["telefone"],
                "observacao": regional.get("observacao", ""),
            }

    return None


def listar_todos_crps():
    dados = _carregar_json("crps.json")
    return dados["regionais"]


def obter_orientacao_denuncia():
    dados = _carregar_json("crps.json")
    return dados["orientacao_denuncia"]


def obter_info_cfp():
    dados = _carregar_json("crps.json")
    return dados["conselho_federal"]


MAPA_ESTADOS = {
    "AC": "Acre", "AL": "Alagoas", "AP": "Amapá", "AM": "Amazonas",
    "BA": "Bahia", "CE": "Ceará", "DF": "Distrito Federal",
    "ES": "Espírito Santo", "GO": "Goiás", "MA": "Maranhão",
    "MT": "Mato Grosso", "MS": "Mato Grosso do Sul", "MG": "Minas Gerais",
    "PA": "Pará", "PB": "Paraíba", "PR": "Paraná", "PE": "Pernambuco",
    "PI": "Piauí", "RJ": "Rio de Janeiro", "RN": "Rio Grande do Norte",
    "RS": "Rio Grande do Sul", "RO": "Rondônia", "RR": "Roraima",
    "SC": "Santa Catarina", "SP": "São Paulo", "SE": "Sergipe",
    "TO": "Tocantins",
}
