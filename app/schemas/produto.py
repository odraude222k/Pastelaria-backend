from pydantic import BaseModel, ConfigDict

class Produto(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str
    preco: float

class ProdutoUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nome: str
    preco:float