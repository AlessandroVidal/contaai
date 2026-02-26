from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    cnpj = Column(String, nullable=False, unique=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="companies")