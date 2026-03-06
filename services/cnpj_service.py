import requests
from fastapi import HTTPException


def get_cnpj_data(cnpj: str):

    url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj}"

    response = requests.get(url)

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

    return {
        "razao_social": data.get("nome"),
        "nome_fantasia": data.get("fantasia"),
        "situacao": data.get("situacao"),
        "logradouro": data.get("logradouro"),
        "numero": data.get("numero"),
        "municipio": data.get("municipio"),
        "uf": data.get("uf"),
    }