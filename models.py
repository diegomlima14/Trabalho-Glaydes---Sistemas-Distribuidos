from sqlalchemy import Column, Integer, Float, String
from database import Base

class Calculo(Base):
    __tablename__ = "calculos"

    id = Column(Integer, primary_key=True, index=True)
    numero1 = Column(Float)
    numero2 = Column(Float)
    operacao = Column(String)
    resultado = Column(Float)
    