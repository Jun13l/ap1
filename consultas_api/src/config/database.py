import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# O Render vai injetar essa variável automaticamente em produção
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://usuario:senha@localhost:5432/consultas_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Gerenciador de sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()