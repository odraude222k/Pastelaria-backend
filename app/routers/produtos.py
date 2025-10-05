from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from ..db_memory import get_db
from .. import models
from ..schemas.produto import (
    Produto as ProdutoSchema,
    ProdutoCreate,
    ProdutoUpdate
)

router = APIRouter(prefix="/produtos",tags=["Produtos"])

@router.get("/", response_model=List[ProdutoSchema])
def listar_produtos(db: Session = Depends(get_db)):
    """
    Busca todos os produtos diretamente do banco de dados.
    """
    produtos = db.query(models.Produto).all()
    return produtos

@router.post("/", response_model=ProdutoSchema, status_code=201)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)): # Usa ProdutoCreate
    """
    Cria um novo produto no banco de dados.
    O ID é gerado automaticamente pelo PostgreSQL.
    """
    # Cria uma instância do modelo SQLAlchemy a partir dos dados do schema Pydantic
    novo_produto = models.Produto(**produto.model_dump())
    
    db.add(novo_produto)  # Adiciona à sessão (prepara para salvar)
    db.commit()           # Salva as mudanças no banco de dados
    db.refresh(novo_produto) # Atualiza o objeto com o ID gerado pelo banco
    
    return novo_produto

@router.put("/{produto_id}", response_model=ProdutoSchema)
def editar_produto(produto_id: int, produto_atualizado: ProdutoUpdate, db: Session = Depends(get_db)):
    """
    Atualiza um produto existente no banco de dados.
    """
    # Primeiro, busca o produto que queremos editar
    produto_query = db.query(models.Produto).filter(models.Produto.id == produto_id)
    produto_existente = produto_query.first()
    
    if not produto_existente:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
        
    # Atualiza o objeto com os novos dados
    # O Pydantic v2 tem um jeito mais elegante para isso, mas o básico funciona bem:
    update_data = produto_atualizado.model_dump(exclude_unset=True)
    produto_query.update(update_data, synchronize_session=False)
    
    db.commit() # Salva as alterações
    
    # Retorna o produto com os dados atualizados
    return produto_query.first()

@router.delete("/{produto_id}", status_code=204) # 204 significa "No Content", uma boa prática para DELETE
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    """
    Deleta um produto do banco de dados.
    """
    produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
        
    db.delete(produto) # Marca o produto para deleção
    db.commit()        # Efetiva a deleção no banco
    
    return {"message": "Produto removido com sucesso"}
