from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.compra import Compra, DetalleCompra
from models.producto import Producto
from app import schemas

def get_compras(db: Session, skip: int = 0, limit: int = 100) -> List[Compra]:
    return db.query(Compra).offset(skip).limit(limit).all()


def create_compra(db: Session, compra: schemas.CompraCreate) -> Compra:
    # 1. Validar productos, calcular total y preparar datos
    total_compra = 0
    productos_info = []

    for item in compra.detalles:
        db_producto = db.query(Producto).filter(Producto.id == item.producto_id).first()
        if not db_producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con id {item.producto_id} no encontrado"
            )
        
        if item.cantidad <= 0 or item.costo_unitario < 0:
            raise HTTPException(status_code=400, detail="Cantidad y costo deben ser positivos.")

        total_compra += item.cantidad * item.costo_unitario
        productos_info.append((db_producto, item.cantidad, item.costo_unitario))

    # Si todos los productos son válidos, procedemos a crear la compra de forma atómica.
    
    # 2. Crear la compra principal
    db_compra = Compra(
        proveedor=compra.proveedor,
        total=total_compra
    )
    db.add(db_compra)
    db.flush()  # Usamos flush para obtener el ID de la compra sin hacer commit todavía.

    # 3. Crear detalles y actualizar stock
    for db_producto, cantidad, costo_unitario in productos_info:
        # Crear el detalle de la compra
        detalle = DetalleCompra(
            compra_id=db_compra.id,
            producto_id=db_producto.id,
            cantidad=cantidad,
            costo_unitario=costo_unitario  # Corregido: Usar el costo de la petición
        )
        db.add(detalle)

        # Actualizar el stock del producto
        db_producto.stock += cantidad

    db.commit()  # Hacemos commit de todo al final (compra, detalles, actualización de stock)
    db.refresh(db_compra)
    return db_compra
