from fastapi import FastAPI
from routes import producto_routes, venta_routes, compra_routes, gasto_routes

app = FastAPI(
    title="Sistema de Gestión para Puesto de Comida Rápida",
    description="API para gestionar ventas, inventario, y más.",
    version="0.1.0"
)

app.include_router(producto_routes.router)
app.include_router(venta_routes.router)
app.include_router(compra_routes.router)
app.include_router(gasto_routes.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido al API del sistema de gestión."}
