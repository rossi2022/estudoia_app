from database import engine, Base

print("📦 Criando o banco de dados...")
Base.metadata.create_all(bind=engine)
print("✅ Banco de dados criado com sucesso.")




