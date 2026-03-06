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
    name: str
    cnpj: str
    user_id: int

    class Config:
        from_attributes = True