from sqlalchemy import Column, Integer, String, Float, DateTime, func
from app.database import Base

class Gasto(Base):
    __tablename__ = "gastos"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String, nullable=False)
    monto = Column(Float, nullable=False)
    fecha = Column(DateTime(timezone=True), server_default=func.now())
    categoria = Column(String, nullable=True, index=True)
