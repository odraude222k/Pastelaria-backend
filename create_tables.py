from app.db_memory import engine, Base
import app.models.models

print("Criando tabelas no banco de dados...")

Base.metadata.create_all(bind=engine)

print("Tabelas criadas com sucesso!")