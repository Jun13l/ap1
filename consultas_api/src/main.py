from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from typing import List
from src.config.database import engine, Base, get_db
from src.models.models import UsuarioCreate, UsuarioResponse, ConsultaCreate, ConsultaResponse
from src.services.service import ServicoConsultas

# Garante a criação automática das tabelas ao iniciar no Render
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Agendamento de Consultas Médicas - Juniel Alves")

@app.get("/")
def endpoint_raiz():
    return {"message": "API de Agendamento de Consultas Online"}

# RF01 e RF02 - Cadastro e Autenticação
@app.post("/auth/register", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED, tags=["Acesso"])
def cadastrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return ServicoConsultas.cadastrar_usuario(db, usuario)

@app.post("/auth/login", tags=["Acesso"])
def logar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return ServicoConsultas.autenticar_usuario(db, usuario)

# RF03 e RF05 - Gerenciamento e Agendamento
@app.post("/consultas", response_model=ConsultaResponse, status_code=status.HTTP_201_CREATED, tags=["Agenda"])
def agendar_consulta(consulta: ConsultaCreate, db: Session = Depends(get_db)):
    return ServicoConsultas.agendar_nova_consulta(db, consulta)

# Relatórios e Histórico
@app.get("/consultas/historico", response_model=List[ConsultaResponse], tags=["Relatórios"])
def visualizar_historico(db: Session = Depends(get_db)):
    return ServicoConsultas.obter_historico(db)

# RF06 - Cancelamento
@app.put("/consultas/{consulta_id}/cancelar", tags=["Controle"])
def cancelar_consulta(consulta_id: int, db: Session = Depends(get_db)):
    return ServicoConsultas.cancelar_agendamento(db, consulta_id)