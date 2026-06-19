from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from src.repositories.repository import RepositorioConsultas
from src.models.models import UsuarioCreate, ConsultaCreate

class ServicoConsultas:
    @staticmethod
    def cadastrar_usuario(db: Session, usuario: UsuarioCreate):
        usuario_existe = RepositorioConsultas.buscar_usuario_por_username(db, usuario.username)
        if usuario_existe:
            raise HTTPException(status_code=400, detail="Usuário já cadastrado.")
        return RepositorioConsultas.criar_usuario(db, usuario)

    @staticmethod
    def autenticar_usuario(db: Session, usuario: UsuarioCreate):
        db_usuario = RepositorioConsultas.buscar_usuario_por_username(db, usuario.username)
        if not db_usuario or db_usuario.password != usuario.password:
            raise HTTPException(status_code=401, detail="Credenciais inválidas.")
        return {"status": "Login funcional efetuado com sucesso"}

    @staticmethod
    def agendar_nova_consulta(db: Session, consulta: ConsultaCreate):
        # Regra de Negócio 1: Não permitir agendamentos para datas passadas.
        if consulta.data_hora < datetime.now():
            raise HTTPException(status_code=400, detail="Não é permitido agendar consultas para datas passadas.")

        # Regra de Negócio 2: Um paciente só pode ter uma consulta ativa por vez.
        consultas_ativas = RepositorioConsultas.buscar_consultas_ativas_por_paciente(db, consulta.paciente_nome)
        if consultas_ativas:
            raise HTTPException(status_code=400, detail="O paciente já possui uma consulta ativa.")

        # Regra de Negócio 4: Respeitar horário de funcionamento da clínica (ex: 08:00 às 18:00).
        if consulta.data_hora.hour < 8 or consulta.data_hora.hour >= 18:
            raise HTTPException(status_code=400, detail="Horário inválido. Funcionamento da clínica é das 08h às 18h.")

        return RepositorioConsultas.criar_agendamento(db, consulta)

    @staticmethod
    def obter_historico(db: Session):
        return RepositorioConsultas.buscar_todas_consultas(db)

    @staticmethod
    def cancelar_agendamento(db: Session, consulta_id: int):
        consulta = RepositorioConsultas.buscar_consulta_por_id(db, consulta_id)
        if not consulta:
            raise HTTPException(status_code=404, detail="Consulta não encontrada.")

        # Regra de Negócio 3: Cancelamentos devem ser feitos com antecedência mínima de 24 horas.
        if datetime.now() + timedelta(hours=24) > consulta.data_hora:
            raise HTTPException(status_code=400, detail="Cancelamento bloqueado. Antecedência mínima de 24h exigida.")

        consulta.ativa = False
        RepositorioConsultas.salvar_alteracoes(db)
        return {"message": "Consulta cancelada com sucesso."}