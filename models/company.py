from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from db import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    cnpj = Column(String(14), nullable=False, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="companies")

    __table_args__ = (
        UniqueConstraint("cnpj", "user_id", name="unique_user_cnpj"),
    )