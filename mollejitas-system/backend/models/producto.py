from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True, nullable=False)
    descripcion = Column(String, nullable=True)
    precio_venta = Column(Float, nullable=False)
    costo_unitario = Column(Float, nullable=False)
    categoria = Column(String, index=True, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
