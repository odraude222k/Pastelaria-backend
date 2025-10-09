from fastapi import FastAPI
from .routers import produtos,carrinho
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Pastelaria da Luzia")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(produtos.router)
app.include_router(carrinho.router)

app.get("/")
def home():
     return {"message": "API da Pastelaria no ar! Projeto organizado."}