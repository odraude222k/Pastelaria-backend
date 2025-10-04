from typing import List
from pydantic import BaseModel
from .produto import Produto

class ItemCarrinhoBase(BaseModel):
    produto_id: int
    quantidade: int

class ItemCarrinho(BaseModel):
    produto: Produto
    quantidade: int
    subtotal: float

class Carrinho(BaseModel):
    itens: List[ItemCarrinho]
    valor_total: float