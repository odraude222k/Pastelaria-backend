from fastapi import APIRouter,HTTPException
from ..db_memory import db_produtos, db_carrinho
from ..schemas.carrinho import Carrinho, ItemCarrinho, ItemCarrinhoBase

router = APIRouter(prefix="/carrinho",tags=["Carrinho"])

@router.get("/", response_model=Carrinho)
def ver_carrinho():
    itens_detalhados = []
    valor_inicial = 0.0
    for item in db_carrinho:
        produto = next((p for p in db_produtos if p.id == item["produto_id"]), None)
        if produto:
            subtotal = produto.preco * item["quantidade"]
            itens_detalhados.append(ItemCarrinho(produto=produto,quantidade = item["quantidade"], subtotal = subtotal))
            valor_total += subtotal
    return Carrinho(itens=itens_detalhados, valor_total=valor_total)

@router.post("/adicionar", response_model=Carrinho)
def adicionar_ao_carrinho(item: ItemCarrinhoBase):
    produto = next((p for p in db_produtos if p.id == item.produto_id), None)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    item_existente = next((i for i in db_carrinho if i["produto_id"] == item.produto_id), None)
    if item_existente:
        item_existente["quantidade"] += item.quantidade
    else:
        db_carrinho.append({"produto_id": item.produto_id, "quantidade": item.quantidade})

    return ver_carrinho

@router.delete("/remover/{produto_id}")
def remover_do_carrinho(produto_id: int):
    item = next((i for i in db_carrinho if i["produto_id"] == produto_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado no carrinho")
    db_carrinho.remove(item)

    return ver_carrinho