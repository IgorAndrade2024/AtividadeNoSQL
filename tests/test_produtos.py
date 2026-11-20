import pytest
import redis

from fastapi.testclient import TestClient
from app.main import app
from app.routes import produtos as produtos_routes


@pytest.fixture
def client(monkeypatch):
    # Banco lógico exclusivo para testes
    redis_teste = redis.Redis(
        host="localhost",
        port=6379,
        db=1,
        decode_responses=True
    )

    # Limpa somente o banco de testes
    redis_teste.flushdb()

    # Substitui a conexão da aplicação pela conexão de testes
    monkeypatch.setattr(
        produtos_routes,
        "redis_client",
        redis_teste
    )

    with TestClient(app) as test_client:
        yield test_client

    # Limpeza após cada teste
    redis_teste.flushdb()
    redis_teste.close()


# CREATE
def test_criar_produto(client):
    resposta = client.post(
        "/produtos/",
        json={
            "nome": "Notebook Dell",
            "preco": 3500,
            "categoria": "Eletronicos",
            "estoque": 12
        }
    )

    assert resposta.status_code == 201
    assert resposta.json()["produto"]["nome"] == "Notebook Dell"


# READ - Listar
def test_listar_produtos(client):
    client.post(
        "/produtos/",
        json={
            "nome": "Mouse Gamer",
            "preco": 150,
            "categoria": "Perifericos",
            "estoque": 20
        }
    )

    resposta = client.get("/produtos/")

    assert resposta.status_code == 200
    assert len(resposta.json()) == 1
    assert resposta.json()[0]["nome"] == "Mouse Gamer"


# READ - Buscar por ID
def test_buscar_produto(client):
    cadastro = client.post(
        "/produtos/",
        json={
            "nome": "Teclado",
            "preco": 200,
            "categoria": "Perifericos",
            "estoque": 10
        }
    )

    produto_id = cadastro.json()["id"]

    resposta = client.get(f"/produtos/{produto_id}")

    assert resposta.status_code == 200
    assert resposta.json()["nome"] == "Teclado"


# UPDATE
def test_atualizar_produto(client):
    cadastro = client.post(
        "/produtos/",
        json={
            "nome": "Monitor",
            "preco": 900,
            "categoria": "Eletronicos",
            "estoque": 5
        }
    )

    produto_id = cadastro.json()["id"]

    resposta = client.put(
        f"/produtos/{produto_id}",
        json={
            "nome": "Monitor Gamer",
            "preco": 1200,
            "categoria": "Eletronicos",
            "estoque": 8
        }
    )

    assert resposta.status_code == 200
    assert resposta.json()["produto"]["nome"] == "Monitor Gamer"


# DELETE
def test_excluir_produto(client):
    cadastro = client.post(
        "/produtos/",
        json={
            "nome": "Headset",
            "preco": 300,
            "categoria": "Audio",
            "estoque": 15
        }
    )

    produto_id = cadastro.json()["id"]

    resposta = client.delete(f"/produtos/{produto_id}")

    assert resposta.status_code == 200

    consulta = client.get(f"/produtos/{produto_id}")

    assert consulta.status_code == 404


# ERRO - Produto inexistente
def test_buscar_produto_inexistente(client):
    resposta = client.get("/produtos/id-inexistente")

    assert resposta.status_code == 404


# ERRO - Atualizar produto inexistente
def test_atualizar_produto_inexistente(client):
    resposta = client.put(
        "/produtos/id-inexistente",
        json={
            "nome": "Produto",
            "preco": 100,
            "categoria": "Teste",
            "estoque": 5
        }
    )

    assert resposta.status_code == 404


# ERRO - Excluir produto inexistente
def test_excluir_produto_inexistente(client):
    resposta = client.delete("/produtos/id-inexistente")

    assert resposta.status_code == 404


# ERRO - Dados inválidos
def test_cadastrar_produto_com_preco_negativo(client):
    resposta = client.post(
        "/produtos/",
        json={
            "nome": "Produto Inválido",
            "preco": -100,
            "categoria": "Teste",
            "estoque": 5
        }
    )

    assert resposta.status_code == 422

# ERRO - Nome com menos de 2 caracteres
def test_cadastrar_produto_com_nome_curto(client):
    resposta = client.post(
        "/produtos/",
        json={
            "nome": "A",
            "preco": 100,
            "categoria": "Teste",
            "estoque": 5
        }
    )

    assert resposta.status_code == 422


# ERRO - Categoria vazia
def test_cadastrar_produto_com_categoria_vazia(client):
    resposta = client.post(
        "/produtos/",
        json={
            "nome": "Produto",
            "preco": 100,
            "categoria": "",
            "estoque": 5
        }
    )

    assert resposta.status_code == 422


# ERRO - Categoria muito longa
def test_cadastrar_produto_com_categoria_longa(client):
    resposta = client.post(
        "/produtos/",
        json={
            "nome": "Produto",
            "preco": 100,
            "categoria": "A" * 51,
            "estoque": 5
        }
    )

    assert resposta.status_code == 422


# ERRO - Preço igual a zero
def test_cadastrar_produto_com_preco_zero(client):
    resposta = client.post(
        "/produtos/",
        json={
            "nome": "Produto",
            "preco": 0,
            "categoria": "Teste",
            "estoque": 5
        }
    )

    assert resposta.status_code == 422


# ERRO - Estoque negativo
def test_cadastrar_produto_com_estoque_negativo(client):
    resposta = client.post(
        "/produtos/",
        json={
            "nome": "Produto",
            "preco": 100,
            "categoria": "Teste",
            "estoque": -1
        }
    )

    assert resposta.status_code == 422


# VALIDAÇÃO - Remover espaços desnecessários
def test_cadastrar_produto_com_espacos(client):
    resposta = client.post(
        "/produtos/",
        json={
            "nome": "  Notebook  ",
            "preco": 3500,
            "categoria": "  Eletronicos  ",
            "estoque": 10
        }
    )

    assert resposta.status_code == 201
    assert resposta.json()["produto"]["nome"] == "Notebook"
    assert resposta.json()["produto"]["categoria"] == "Eletronicos"

# ERRO - Redis indisponível
def test_redis_indisponivel(client, monkeypatch):

    def simular_falha(*args, **kwargs):
        raise redis.ConnectionError(
            "Redis indisponível"
        )

    monkeypatch.setattr(
        produtos_routes.redis_client,
        "scan_iter",
        simular_falha
    )

    resposta = client.get("/produtos/")

    assert resposta.status_code == 503
    assert resposta.json()["erro"] == (
        "Serviço temporariamente indisponível"
    )
