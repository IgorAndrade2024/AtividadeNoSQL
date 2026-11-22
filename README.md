# CRUD de Produtos com Redis

API REST desenvolvida em Python utilizando **FastAPI** e **Redis** para gerenciamento de produtos. O projeto implementa as operações CRUD (Create, Read, Update e Delete), validação de dados, tratamento de erros, persistência e testes automatizados.




## Tecnologias utilizadas

- **Python 3.14** — linguagem de programação.
- **FastAPI** — framework para desenvolvimento da API REST.
- **Redis 8** — banco de dados NoSQL em memória.
- **Redis Hashes** — estrutura utilizada para armazenar os produtos.
- **Pydantic** — validação dos dados recebidos pela API.
- **Pytest** — execução dos testes automatizados.
- **HTTPX** — suporte aos testes de integração.

## Funcionalidades

- Cadastro de produtos.
- Listagem de todos os produtos.
- Busca de produto por identificador.
- Atualização de produtos existentes.
- Exclusão de produtos.
- Validação dos dados de entrada.
- Tratamento de indisponibilidade do Redis.
- Persistência de dados utilizando RDB e AOF.
- Testes automatizados das operações e dos cenários de erro.

## Estrutura do projeto

```text
crud-redis/
│
├── app/
│   ├── routes/
│   │   ├── __init__.py
│   │   └── produtos.py
│   │
│   ├── __init__.py
│   ├── database.py
│   ├── exceptions.py
│   ├── main.py
│   └── models.py
│
├── tests/
│   ├── __init__.py
│   └── test_produtos.py
│
├── .venv/
├── requirements.txt
└── README.md
```

## Pré-requisitos

Antes de executar o projeto, é necessário ter instalado:

- Python 3.12 ou superior.
- Redis Server.
- pip.
- Git (opcional).

## Instalação

### 1. Clonar o repositório

```bash
git clone URL_DO_REPOSITORIO
cd crud-redis
```

Caso já tenha o projeto localmente, entre diretamente no diretório:

```bash
cd crud-redis
```

### 2. Criar o ambiente virtual

```bash
python3 -m venv .venv
```

Ativar o ambiente virtual no Linux:

```bash
source .venv/bin/activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

## Configuração do Redis

Inicie o serviço Redis:

```bash
sudo systemctl start redis-server
```

Configure a inicialização automática:

```bash
sudo systemctl enable redis-server
```

Verifique se o serviço está funcionando:

```bash
sudo systemctl status redis-server
```

Teste a conexão:

```bash
redis-cli ping
```

Resposta esperada:

```text
PONG
```

### Configuração da persistência

O projeto utiliza os mecanismos de persistência do Redis:

**RDB (Redis Database Backup)**

Realiza snapshots dos dados em intervalos configurados.

Arquivo padrão:

```text
/var/lib/redis/dump.rdb
```

**AOF (Append Only File)**

Registra as operações de escrita para permitir a recuperação dos dados.

Configurações utilizadas:

```conf
appendonly yes
appendfsync everysec
```

Com `appendfsync everysec`, o Redis sincroniza o AOF aproximadamente a cada segundo.

## Executando a aplicação

Com o ambiente virtual ativado e o Redis em execução, inicie a API:

```bash
uvicorn app.main:app --reload
```

A aplicação ficará disponível em:

```text
http://127.0.0.1:8000
```

### Documentação interativa

O FastAPI disponibiliza uma interface Swagger para testar os endpoints:

```text
http://127.0.0.1:8000/docs
```

Também é possível acessar a documentação alternativa:

```text
http://127.0.0.1:8000/redoc
```

## Endpoints da API

A API disponibiliza os seguintes endpoints:

| Método HTTP | Endpoint | Descrição |
|---|---|---|
| GET | `/` | Verifica o funcionamento da API |
| GET | `/health` | Verifica a conexão com o Redis |
| POST | `/produtos/` | Cadastra um produto |
| GET | `/produtos/` | Lista todos os produtos |
| GET | `/produtos/{produto_id}` | Busca um produto pelo ID |
| PUT | `/produtos/{produto_id}` | Atualiza um produto |
| DELETE | `/produtos/{produto_id}` | Exclui um produto |

### Modelo de produto

Os produtos possuem os seguintes atributos:

| Campo | Tipo | Validação |
|---|---|---|
| nome | String | Entre 2 e 100 caracteres |
| preco | Float | Maior que zero |
| categoria | String | Entre 2 e 50 caracteres |
| estoque | Integer | Maior ou igual a zero |

### Exemplo de cadastro

Requisição:

```http
POST /produtos/
```

Corpo JSON:

```json
{
    "nome": "Notebook Dell",
    "preco": 3500,
    "categoria": "Eletronicos",
    "estoque": 12
}
```

Resposta esperada:

```json
{
    "mensagem": "Produto cadastrado com sucesso!",
    "id": "identificador-gerado",
    "produto": {
        "nome": "Notebook Dell",
        "preco": 3500,
        "categoria": "Eletronicos",
        "estoque": 12
    }
}
```

O identificador do produto é gerado automaticamente utilizando UUID.

## Estrutura de armazenamento no Redis

Os produtos são armazenados utilizando a estrutura **Hash** do Redis.

Cada produto possui uma chave própria, seguindo o padrão:

```text
produto:{produto_id}
```

Exemplo:

```text
produto:d9365b13-0627-4125-a3c7-d1a8cdb12cb3
```

Os atributos são armazenados como campos do Hash:

```text
nome       -> Notebook Dell
preco      -> 3500.0
categoria  -> Eletronicos
estoque    -> 12
```

Essa estrutura permite consultar e atualizar os atributos individualmente utilizando os comandos do Redis.

## Testes automatizados

O projeto utiliza **Pytest** para validar as operações da API.

Para executar os testes:

```bash
pytest -v
```

Os testes utilizam o banco lógico Redis DB 1, separado do banco principal da aplicação (DB 0).

A fixture de testes limpa o banco de testes antes e depois de cada execução.

### Cenários testados

- Cadastro de produtos.
- Listagem de produtos.
- Busca por identificador.
- Atualização de produtos.
- Exclusão de produtos.
- Busca de produto inexistente.
- Atualização de produto inexistente.
- Exclusão de produto inexistente.
- Cadastro com preço negativo.
- Cadastro com nome inválido.
- Cadastro com categoria vazia.
- Cadastro com categoria acima do limite.
- Cadastro com preço igual a zero.
- Cadastro com estoque negativo.
- Remoção de espaços desnecessários.
- Simulação de indisponibilidade do Redis.

**Último resultado registrado:** 16 testes aprovados.

## Tratamento de erros

A API implementa tratamento para falhas de comunicação com o Redis.

Quando o banco de dados está indisponível, a aplicação retorna:

```http
503 Service Unavailable
```

Exemplo de resposta:

```json
{
    "erro": "Serviço temporariamente indisponível",
    "mensagem": "Não foi possível acessar o banco de dados Redis."
}
```

Também são utilizados códigos HTTP para indicar situações como recursos inexistentes e dados inválidos:

- `201` — Recurso criado.
- `200` — Requisição executada com sucesso.
- `404` — Produto não encontrado.
- `422` — Dados enviados inválidos.
- `503` — Serviço Redis indisponível.

## Objetivo acadêmico

Este projeto tem como objetivo aplicar conceitos de desenvolvimento de APIs REST e utilização de bancos de dados NoSQL, explorando o Redis como mecanismo de armazenamento de dados.

A implementação permite estudar operações CRUD, estruturas de dados Hash, validação de informações, persistência, tratamento de exceções e testes automatizados utilizando Python.

---

**Projeto acadêmico — CRUD com Redis**

Desenvolvido utilizando Python, FastAPI e Redis.
