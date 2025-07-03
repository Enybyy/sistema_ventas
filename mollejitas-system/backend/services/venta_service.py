from sqlalchemy.orm import Session
from models.venta import Venta, DetalleVenta
from models.producto import Producto
from app.schemas import VentaCreate

def create_venta(db: Session, venta: VentaCreate) -> Venta:
    total_venta = 0
    db_detalles = []

    # Primero, calcula el total y valida los productos
    for detalle in venta.detalles:
        producto = db.query(Producto).filter(Producto.id == detalle.producto_id).first()
        if not producto:
            raise ValueError(f"Producto con id {detalle.producto_id} no encontrado")
        
        subtotal = producto.precio_venta * detalle.cantidad
        total_venta += subtotal
        
        db_detalles.append({
            "producto_id": detalle.producto_id,
            "cantidad": detalle.cantidad,
            "precio_unitario": producto.precio_venta,
            "subtotal": subtotal
        })

    # Crea la venta principal
    db_venta = Venta(total=total_venta)
    db.add(db_venta)
    db.flush() # Para obtener el id de la venta antes de commit

    # Crea los detalles de la venta
    for detalle_data in db_detalles:
        db_detalle = DetalleVenta(**detalle_data, venta_id=db_venta.id)
        db.add(db_detalle)

    db.commit()
    db.refresh(db_venta)
    return db_venta

def get_venta(db: Session, venta_id: int):
    return db.query(Venta).filter(Venta.id == venta_id).first()

def get_ventas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Venta).offset(skip).limit(limit).all()
