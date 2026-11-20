from pydantic import BaseModel, Field, ConfigDict


class Produto(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True
    )

    nome: str = Field(
        min_length=2,
        max_length=100
    )

    preco: float = Field(
        gt=0,
        allow_inf_nan=False
    )

    categoria: str = Field(
        min_length=2,
        max_length=50
    )

    estoque: int = Field(
        ge=0
    )

