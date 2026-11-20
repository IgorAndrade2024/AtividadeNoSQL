from fastapi import APIRouter, HTTPException
from app.database import redis_client
from app.models import Produto
import uuid

router = APIRouter(
    prefix="/produtos",
    tags=["Produtos"]
)


# CREATE - Cadastrar produto
@router.post("/", status_code=201)
def criar_produto(produto: Produto):
    produto_id = str(uuid.uuid4())
    dados = produto.model_dump()

    redis_client.hset(
        f"produto:{produto_id}",
        mapping={
            chave: str(valor)
            for chave, valor in dados.items()
        }
    )

    return {
        "mensagem": "Produto cadastrado com sucesso!",
        "id": produto_id,
        "produto": dados
    }


# READ - Listar todos os produtos
@router.get("/")
def listar_produtos():
    produtos = []

    for chave in redis_client.scan_iter("produto:*"):
        dados = redis_client.hgetall(chave)

        produtos.append({
            "id": chave.replace("produto:", ""),
            "nome": dados["nome"],
            "preco": float(dados["preco"]),
            "categoria": dados["categoria"],
            "estoque": int(dados["estoque"])
        })

    return produtos


# READ - Buscar produto por ID
@router.get("/{produto_id}")
def buscar_produto(produto_id: str):
    chave = f"produto:{produto_id}"
    dados = redis_client.hgetall(chave)

    if not dados:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    return {
        "id": produto_id,
        "nome": dados["nome"],
        "preco": float(dados["preco"]),
        "categoria": dados["categoria"],
        "estoque": int(dados["estoque"])
    }


# UPDATE - Atualizar produto
@router.put("/{produto_id}")
def atualizar_produto(produto_id: str, produto: Produto):
    chave = f"produto:{produto_id}"

    if not redis_client.exists(chave):
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    dados = produto.model_dump()

    redis_client.hset(
        chave,
        mapping={
            campo: str(valor)
            for campo, valor in dados.items()
        }
    )

    return {
        "mensagem": "Produto atualizado com sucesso!",
        "id": produto_id,
        "produto": dados
    }


# DELETE - Excluir produto
@router.delete("/{produto_id}")
def excluir_produto(produto_id: str):
    chave = f"produto:{produto_id}"
    resultado = redis_client.delete(chave)

    if resultado == 0:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    return {
        "mensagem": "Produto excluído com sucesso!",
        "id": produto_id
    }
