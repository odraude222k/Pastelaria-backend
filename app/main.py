from fastapi import FastAPI
from .routers import produtos,carrinho
app = FastAPI(title="Pastelaria da Luzia")

app.include_router(produtos.router)
app.include_router(carrinho.router)

app.get("/")
def home():
     return {"message": "API da Pastelaria no ar! Projeto organizado."}