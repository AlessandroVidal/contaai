import requests
from fastapi import HTTPException


def get_cnpj_data(cnpj: str):

    url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj}"
import requests
from fastapi import HTTPException


def get_cnpj_data(cnpj: str):

    url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj}"

    try:
        response = requests.get(url, timeout=10)
    except requests.RequestException:
        raise HTTPException(
            status_code=500,
            detail="Erro ao conectar com serviço de CNPJ"
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=400,
            detail="Erro ao consultar CNPJ"
        )

    data = response.json()

    if data.get("status") == "ERROR":
        raise HTTPException(
            status_code=400,
            detail="CNPJ inválido ou não encontrado"
        )

    atividade = None
    if data.get("atividade_principal"):
        atividade = data["atividade_principal"][0]["text"]

    return {
        "razao_social": data.get("nome"),
        "nome_fantasia": data.get("fantasia"),
        "situacao": data.get("situacao"),

        "logradouro": data.get("logradouro"),
        "numero": data.get("numero"),
        "bairro": data.get("bairro"),

        "municipio": data.get("municipio"),
        "uf": data.get("uf"),
        "cep": data.get("cep"),

        "atividade_principal": atividade,
        "data_abertura": data.get("abertura"),
    }
   