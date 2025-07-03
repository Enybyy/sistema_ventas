from fastapi import FastAPI

app = FastAPI(title="Sistema de Gestión para Puesto de Comida Rápida")

@app.get("/")
def read_root():
    return {"message": "Bienvenido al API del sistema de gestión."}
