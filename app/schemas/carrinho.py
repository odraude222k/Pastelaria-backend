from typing import List
from pydantic import BaseModel, ConfigDict
from .produto import Produto

class ItemCarrinhoBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    produto_id: int
    quantidade: int

class ItemCarrinho(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    produto: Produto
    quantidade: int
    subtotal: float

class Carrinho(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    itens: List[ItemCarrinho]
    valor_total: float

class ItemRemover(BaseModel):
    produto_id: int
    quantidade: int