import redis

# Configuração da conexão com o Redis
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)

# Verifica se a conexão está funcionando
def verificar_conexao():
    try:
        return redis_client.ping()
    except redis.ConnectionError:
        return False
