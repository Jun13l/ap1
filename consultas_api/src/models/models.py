from sqlalchemy import Column, Integer, String, DateTime, Boolean
from src.config.database import Base
from pydantic import BaseModel
from datetime import datetime

# --- TABELAS DO BANCO DE DADOS (SQLAlchemy) ---
class UsuarioModel(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

class ConsultaModel(Base):
    __tablename__ = "consultas"
    id = Column(Integer, primary_key=True, index=True)
    paciente_nome = Column(String, index=True)
    data_hora = Column(DateTime)
    ativa = Column(Boolean, default=True)

# --- VALIDAÇÃO DE DADOS (Pydantic) ---
class UsuarioCreate(BaseModel):
    username: str
    password: str

class UsuarioResponse(BaseModel):
    id: int
    username: str
    class Config:
        from_attributes = True

class ConsultaCreate(BaseModel):
    paciente_nome: str
    data_hora: datetime

class ConsultaResponse(BaseModel):
    id: int
    paciente_nome: str
    data_hora: datetime
    ativa: bool
    class Config:
        from_attributes = True