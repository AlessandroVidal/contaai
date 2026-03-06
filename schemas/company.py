from pydantic import BaseModel, field_validator


class CompanyCreate(BaseModel):
    cnpj: str

    @field_validator("cnpj")
    def validate_cnpj(cls, value):

        cnpj = value.replace(".", "").replace("/", "").replace("-", "")

        if not cnpj.isdigit() or len(cnpj) != 14:
            raise ValueError("CNPJ inválido")

        return cnpj


class CompanyResponse(BaseModel):

    id: int
    user_id: int

    cnpj: str
    razao_social: str
    nome_fantasia: str

    situacao: str

    logradouro: str
    numero: str
    bairro: str

    municipio: str
    uf: str
    cep: str

    atividade_principal: str
    data_abertura: str

    class Config:
        from_attributes = True