from pydantic import BaseModel

class Produto(BaseModel):
    id: int
    nome: str
    preco: float

db_produtos = [
    Produto(id=1, nome="Pastel de Carne", preco=8.50),
    Produto(id=2, nome="Pastel de Queijo", preco=8.00),
    Produto(id=3, nome="Caldo de Cana", preco=6.00),
]

db_carrinho = []