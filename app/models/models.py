from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from ..db_memory import Base

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True)
    descricao = Column(String, nullable=True) 
    preco = Column(Float)

    # Relacionamento para acessar os itens do pedido associados a este produto
    itens_pedido = relationship("ItemPedido", back_populates="produto")


class ItemCarrinho(Base):
    """
    Representa um item no carrinho de compras.
    Esta tabela pode ser limpa periodicamente ou quando um pedido é criado.
    """
    __tablename__ = "itens_carrinho"

    id = Column(Integer, primary_key=True, index=True)
    quantidade = Column(Integer, nullable=False)
    
    # Chave estrangeira para linkar com a tabela de produtos
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    
    # Relacionamento para acessar o objeto Produto a partir do ItemCarrinho
    produto = relationship("Produto") 

class Pedido(Base):
    """
    Representa um pedido finalizado pelo cliente.
    """
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    nome_cliente = Column(String, nullable=False)
    telefone_cliente = Column(String) # Pode ser opcional
    status = Column(String, default="Pendente") # Ex: Pendente, Aceito, Em Preparo, Finalizado
    valor_total = Column(Float)
    data_criacao = Column(DateTime, default=func.now()) # Registra a data/hora da criação

    # Relacionamento para acessar a lista de itens deste pedido.
    # `cascade="all, delete-orphan"`: Se um pedido for deletado,
    # todos os seus itens são deletados automaticamente.
    itens = relationship("ItemPedido", back_populates="pedido", cascade="all, delete-orphan")

class ItemPedido(Base):
    """
    Representa um item específico dentro de um pedido finalizado.
    """
    __tablename__ = "itens_pedido"

    id = Column(Integer, primary_key=True, index=True)
    quantidade = Column(Integer, nullable=False)
    
    # Guarda o preço no momento da compra para o histórico não mudar
    # se o preço do produto for alterado no futuro.
    preco_unitario = Column(Float, nullable=False)

    # Chave estrangeira para linkar com a tabela de pedidos
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))
    
    # Chave estrangeira para linkar com a tabela de produtos
    produto_id = Column(Integer, ForeignKey("produtos.id"))

    # Relacionamentos para navegar para o Pedido e para o Produto
    pedido = relationship("Pedido", back_populates="itens")
    produto = relationship("Produto", back_populates="itens_pedido")

