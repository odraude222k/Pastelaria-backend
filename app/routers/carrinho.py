from fastapi import APIRouter,HTTPException
from ..db_memory import db_produtos, db_carrinho
from ..schemas.carrinho import Carrinho, ItemCarrinho, ItemCarrinhoBase,ItemRemover


router = APIRouter(prefix="/carrinho",tags=["Carrinho"])

@router.get("/", response_model=Carrinho)
def ver_carrinho():
    itens_detalhados = []
    valor_total = 0.0
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

    return ver_carrinho()

@router.post("/remover",response_model=Carrinho)
def remover_do_carrinho(item_a_remover: ItemRemover):
    item_encontrado = None
    for item_no_carrinho in db_carrinho:
        if item_no_carrinho['produto_id'] == item_a_remover.produto_id:
            item_encontrado = item_no_carrinho
            break

    if not item_encontrado:
        raise HTTPException(status_code=404, detail="Produto não encontrado no carrinho")
        
    if item_a_remover.quantidade >= item_encontrado['quantidade']:
        db_carrinho.remove(item_encontrado)
    else:
        item_encontrado['quantidade'] -= item_a_remover.quantidade
        
    return ver_carrinho()
