from pydantic import BaseModel, ConfigDict


class ProdutoBase(BaseModel):
    nome: str
    preco: float

class ProdutoCreate(ProdutoBase):
    pass

class Produto(ProdutoBase):
    id: int 
    model_config = ConfigDict(from_attributes=True)

class ProdutoUpdate(ProdutoBase):
    pass