from fastapi import Request
from fastapi.responses import JSONResponse
from redis.exceptions import RedisError


async def redis_exception_handler(
    request: Request,
    exc: RedisError
):
    return JSONResponse(
        status_code=503,
        content={
            "erro": "Serviço temporariamente indisponível",
            "mensagem": "Não foi possível acessar o banco de dados Redis."
        }
    )
