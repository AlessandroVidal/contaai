from pydantic import BaseModel


class CompanyCreate(BaseModel):
    name: str
    cnpj: str


class CompanyResponse(BaseModel):
    id: int
    name: str
    cnpj: str

    class Config:
        from_attributes = True