from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    cnpj = Column(String, index=True)

    razao_social = Column(String)
    nome_fantasia = Column(String)

    situacao = Column(String)

    logradouro = Column(String)
    numero = Column(String)
    bairro = Column(String)

    municipio = Column(String)
    uf = Column(String)

    cep = Column(String)

    atividade_principal = Column(String)
    data_abertura = Column(String)

    owner = relationship("User", back_populates="companies")