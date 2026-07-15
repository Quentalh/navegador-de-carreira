import uuid
import enum
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Numeric, Float, text
from sqlalchemy.dialects.postgresql import JSONB, UUID, ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.db.models.base import Base

class PlanoEnum(str, enum.Enum):
    free = "free"
    premium = "premium"

class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    senha_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    
    disponibilidade_financeira_mensal: Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True)
    cidade: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    estado: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    perfil_estruturado_json: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    plano: Mapped[PlanoEnum] = mapped_column(ENUM(PlanoEnum, name="plano_enum"), nullable=False, default=PlanoEnum.free)
    
    criado_em: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    atualizado_em: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    curriculos: Mapped[list["Curriculo"]] = relationship(back_populates="usuario", cascade="all, delete-orphan")
    roadmaps: Mapped[list["Roadmap"]] = relationship(back_populates="usuario", cascade="all, delete-orphan")
    assinaturas: Mapped[list["Assinatura"]] = relationship(back_populates="usuario", cascade="all, delete-orphan")
