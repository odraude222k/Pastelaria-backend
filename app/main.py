from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Pastelaria da Luzia")

class Produto(BaseModel):
    id: int
    nome: str
    preco: float

class ProdutoUpdate(BaseModel):
    nome: str
    preco:float

db_produtos = [
    Produto(id=1, nome="Pastel de Carne", preco=8.50),
    Produto(id=2, nome="Pastel de Queijo", preco=8.00),
    Produto(id=3, nome="Caldo de Cana", preco=6.00),
]

@app.get("/")
def home():
    """Endpoint raiz para mostrar que a API está no ar."""
    return {"message": "Bem-vindo à API da Pastelaria!"}

@app.get("/produtos", response_model=List[Produto])
def listar_produtos():
    """Retorna uma lista de todos os produtos cadastrados."""
    return db_produtos

@app.post("/produtos", response_model=Produto, status_code=201)
def criar_produto(produto: Produto):
    """Adiciona um novo produto à lista."""
    db_produtos.append(produto)
    return produto

@app.delete("/produtos/{produto_id}")
def deletar_produto(produto_id: int):
    """Deleta um produto da lista com base no seu ID."""
    produto_para_deletar = None
    for produto in db_produtos:
        if produto.id == produto_id:
            produto_para_deletar = produto
            break

    # Se, após o loop, não encontrarmos o produto, retornamos um erro 404
    if not produto_para_deletar:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    # Se encontrarmos o produto, o removemos da lista
    db_produtos.remove(produto_para_deletar)

    # Retornamos uma mensagem de sucesso
    return {"message": "Produto removido com sucesso"}

@app.put("/produtos/{produto_id}", response_model=Produto)
def editar_produto(produto_id: int, produto_atualizado: ProdutoUpdate):
    index_do_produto = -1
    for i, p in enumerate(db_produtos):
        if p.id == produto_id:
            index_do_produto = i
            break
            
    if index_do_produto == -1:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    produto_existente = db_produtos[index_do_produto]
    
    produto_existente.nome = produto_atualizado.nome
    produto_existente.preco = produto_atualizado.preco
    
    return produto_existente
