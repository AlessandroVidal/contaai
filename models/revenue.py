from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from db import Base


class Revenue(Base):
    __tablename__ = "revenues"

    id = Column(Integer, primary_key=True, index=True)

    company_id = Column(Integer, ForeignKey("companies.id"))
    month = Column(Date)

    revenue = Column(Float)

    company = relationship("Company")