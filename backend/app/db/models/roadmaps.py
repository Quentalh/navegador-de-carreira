import uuid
import enum
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, ForeignKey, Table, Column
from sqlalchemy.dialects.postgresql import JSONB, UUID, ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.db.models.base import Base

class StatusRoadmapEnum(str, enum.Enum):
    gerando = "gerando"
    pronto = "pronto"
    erro = "erro"

# Associative table for roadmaps and vagas
roadmap_vagas = Table(
    "roadmap_vagas",
    Base.metadata,
    Column("roadmap_id", Integer, ForeignKey("roadmaps.id", ondelete="CASCADE"), primary_key=True),
    Column("vaga_id", Integer, ForeignKey("vagas.id", ondelete="CASCADE"), primary_key=True)
)

class Roadmap(Base):
    __tablename__ = "roadmaps"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    usuario_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    proximo_cargo_sugerido: Mapped[str] = mapped_column(String(255), nullable=False)
    tempo_estimado_meses: Mapped[int] = mapped_column(Integer, nullable=False)
    
    passos_json: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    status: Mapped[StatusRoadmapEnum] = mapped_column(ENUM(StatusRoadmapEnum, name="status_roadmap_enum"), nullable=False, default=StatusRoadmapEnum.gerando)
    
    criado_em: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    atualizado_em: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now(), nullable=False)

    usuario: Mapped["Usuario"] = relationship(back_populates="roadmaps")
    vagas: Mapped[list["Vaga"]] = relationship(secondary=roadmap_vagas)
