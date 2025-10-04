from fastapi import APIRouter, HTTPException
from typing import List
from ..db_memory import db_produtos
from ..schemas.produto import Produto,ProdutoUpdate

router = APIRouter(prefix="/produtos",tags=["Produtos"])

@router.get("/", response_model=List[Produto])
def listar_produtos():
    return db_produtos

@router.post("/", response_model=Produto, status_code=201)
def criar_produto(produto: Produto):
    db_produtos.append(produto)
    return produto

@router.put("/{produto_id}",response_model=Produto)
def editar_produto(produto_id: int, produto_atualizado: ProdutoUpdate):
    idx = next((i for i, p in enumerate(db_produtos) if p.id == produto_id), -1)
    if idx == -1:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    produto_existente = db_produtos[idx]
    produto_existente.nome = produto_atualizado.nome
    produto_existente.preco = produto_atualizado.preco
    return produto_existente

@router.delete("/{produto_id}")
def deletar_produto(produto_id: int):
    produto = next((p for p in db_produtos if p.id == produto_id), None)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    db_produtos.remove(produto)
    return {"message": "Produto removido com sucesso"}
