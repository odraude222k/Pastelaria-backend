from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from ..db_memory import get_db
from .. import models
from ..schemas.carrinho import ItemCarrinho,ItemRemover,Carrinho,ItemCarrinhoBase

router = APIRouter(prefix="/carrinho",tags=["Carrinho"])

def obter_carrinho_completo(db: Session):
    """
    Busca todos os itens do carrinho no banco de dados, calcula os totais
    e formata a resposta usando os schemas do Pydantic.
    """
    # 1. Busca todos os itens da tabela 'itens_carrinho'
    itens_no_banco = db.query(models.ItemCarrinho).all()
    
    itens_detalhados = []
    valor_total = 0.0

    # 2. Itera sobre os resultados do banco para montar a resposta
    for item in itens_no_banco:
        # Graças ao `relationship` no models.py, podemos acessar item.produto diretamente
        subtotal = item.produto.preco * item.quantidade
        
        # Monta o objeto de resposta para cada item
        itens_detalhados.append(ItemCarrinho(
            produto=item.produto,
            quantidade=item.quantidade,
            subtotal=subtotal
        ))
        valor_total += subtotal
        
    # 3. Retorna o objeto Carrinho completo
    return Carrinho(itens=itens_detalhados, valor_total=valor_total)

@router.get("/", response_model=Carrinho)
def ver_carrinho(db: Session = Depends(get_db)):
    """
    Endpoint para visualizar o estado atual do carrinho.
    """
    return obter_carrinho_completo(db)

@router.post("/adicionar", response_model=Carrinho)
def adicionar_ao_carrinho(item_a_adicionar: ItemCarrinhoBase, db: Session = Depends(get_db)):
    """
    Adiciona um produto ao carrinho ou incrementa sua quantidade se já existir.
    """
    # Verifica se o produto que estamos tentando adicionar realmente existe
    produto = db.query(models.Produto).filter(models.Produto.id == item_a_adicionar.produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    # Procura pelo item na tabela do carrinho
    item_existente = db.query(models.ItemCarrinho).filter(
        models.ItemCarrinho.produto_id == item_a_adicionar.produto_id
    ).first()
    
    if item_existente:
        # Se o item já existe, apenas soma a quantidade
        item_existente.quantidade += item_a_adicionar.quantidade
    else:
        # Se não existe, cria uma nova instância do modelo e a adiciona
        novo_item = models.ItemCarrinho(**item_a_adicionar.model_dump())
        db.add(novo_item)

    db.commit() # Salva as alterações no banco

    # Retorna o carrinho atualizado chamando nossa função auxiliar
    return obter_carrinho_completo(db)


@router.post("/remover", response_model=Carrinho)
def remover_do_carrinho(item_a_remover: ItemRemover, db: Session = Depends(get_db)):
    """
    Remove uma certa quantidade de um produto do carrinho ou o remove completamente.
    """
    # Busca o item no carrinho no banco de dados
    item_encontrado = db.query(models.ItemCarrinho).filter(
        models.ItemCarrinho.produto_id == item_a_remover.produto_id
    ).first()

    if not item_encontrado:
        raise HTTPException(status_code=404, detail="Produto não encontrado no carrinho")
    
    # Lógica para decidir se removemos o registro ou apenas diminuímos a quantidade
    if item_a_remover.quantidade >= item_encontrado.quantidade:
        db.delete(item_encontrado) # Remove o registro da tabela
    else:
        item_encontrado.quantidade -= item_a_remover.quantidade # Apenas atualiza a quantidade

    db.commit() # Salva as alterações

    # Retorna o carrinho atualizado
    return obter_carrinho_completo(db)
