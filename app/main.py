from fastapi import FastAPI
from app.database import verificar_conexao
from app.routes.produtos import router as produtos_router
from redis.exceptions import RedisError
from app.exceptions import redis_exception_handler

app = FastAPI(
    title="CRUD Redis",
    description="API de gerenciamento de produtos utilizando Redis",
    version="1.0.0"
)

app.add_exception_handler(
    RedisError,
    redis_exception_handler
)

@app.get("/")
def inicio():
    return {
        "mensagem": "API CRUD Redis funcionando!"
    }


@app.get("/health")
def health():
    conectado = verificar_conexao()

    return {
        "api": "online",
        "redis": "conectado" if conectado else "desconectado"
    }


# Registra as rotas de produtos
app.include_router(produtos_router)
