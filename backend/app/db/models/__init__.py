from app.db.models.base import Base
from app.db.models.usuarios import Usuario, PlanoEnum
from app.db.models.curriculos import Curriculo
from app.db.models.vagas import Vaga, FonteVagaEnum
from app.db.models.trajetorias import Trajetoria, FonteDadoEnum
from app.db.models.roadmaps import Roadmap, StatusRoadmapEnum, roadmap_vagas
from app.db.models.clusters import Cluster
from app.db.models.assinaturas import Assinatura, StatusPagamentoEnum

# Export all models for Alembic to find them easily in env.py
__all__ = [
    "Base",
    "Usuario",
    "PlanoEnum",
    "Curriculo",
    "Vaga",
    "FonteVagaEnum",
    "Trajetoria",
    "FonteDadoEnum",
    "Roadmap",
    "StatusRoadmapEnum",
    "roadmap_vagas",
    "Cluster",
    "Assinatura",
    "StatusPagamentoEnum",
]
