from sqlalchemy.orm import Session
from src.models.models import UsuarioModel, ConsultaModel, UsuarioCreate, ConsultaCreate

class RepositorioConsultas:
    @staticmethod
    def criar_usuario(db: Session, usuario: UsuarioCreate):
        db_usuario = UsuarioModel(username=usuario.username, password=usuario.password)
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        return db_usuario

    @staticmethod
    def buscar_usuario_por_username(db: Session, username: str):
        return db.query(UsuarioModel).filter(UsuarioModel.username == username).first()

    @staticmethod
    def criar_agendamento(db: Session, consulta: ConsultaCreate):
        db_consulta = ConsultaModel(paciente_nome=consulta.paciente_nome, data_hora=consulta.data_hora)
        db.add(db_consulta)
        db.commit()
        db.refresh(db_consulta)
        return db_consulta

    @staticmethod
    def buscar_consultas_ativas_por_paciente(db: Session, paciente_nome: str):
        return db.query(ConsultaModel).filter(
            ConsultaModel.paciente_nome == paciente_nome,
            ConsultaModel.ativa == True
        ).all()

    @staticmethod
    def buscar_todas_consultas(db: Session):
        return db.query(ConsultaModel).all()

    @staticmethod
    def buscar_consulta_por_id(db: Session, consulta_id: int):
        return db.query(ConsultaModel).filter(ConsultaModel.id == consulta_id).first()

    @staticmethod
    def salvar_alteracoes(db: Session):
        db.commit()