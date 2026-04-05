from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import engine, Base
from app.core.config import settings

# Importar routers
from app.api.v1.catalogos import marcas, modelos, versiones, tipos_cliente
from app.api.v1.inventario import vehiculos, piezas, compatibilidad
from app.api.v1.ventas import clientes, ventas, reportes

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/")
def root():
    return {
        "message": "API Autopartes Usadas funcionando",
        "status": "online",
        "version": settings.APP_VERSION
    }

@app.get("/health")
def health_check():
    return {"status": "OK"}

# Registrar routers
app.include_router(marcas.router)
app.include_router(modelos.router)
app.include_router(versiones.router)
app.include_router(tipos_cliente.router)
app.include_router(vehiculos.router)
app.include_router(piezas.router)
app.include_router(compatibilidad.router)
app.include_router(clientes.router)
app.include_router(ventas.router)
app.include_router(reportes.router)