import enum
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Numeric, Boolean, Index
from sqlalchemy.dialects.postgresql import JSONB, ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.db.models.base import Base

class FonteVagaEnum(str, enum.Enum):
    linkedin = "linkedin"
    glassdoor = "glassdoor"
    outro = "outro"

class Vaga(Base):
    __tablename__ = "vagas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    titulo_cargo: Mapped[str] = mapped_column(String(255), nullable=False)
    empresa: Mapped[str] = mapped_column(String(255), nullable=False)
    cidade: Mapped[str] = mapped_column(String(100), nullable=False)
    estado: Mapped[str] = mapped_column(String(50), nullable=False)
    
    faixa_salarial_min: Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True)
    faixa_salarial_max: Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True)
    
    requisitos: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    fonte: Mapped[FonteVagaEnum] = mapped_column(ENUM(FonteVagaEnum, name="fonte_vaga_enum"), nullable=False)
    
    url_original: Mapped[str] = mapped_column(String(1000), nullable=False, unique=True, index=True)
    hash_deduplicacao: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    ativa: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    coletada_em: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    criado_em: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)

    __table_args__ = (
        Index("ix_vagas_cidade_titulo_cargo", "cidade", "titulo_cargo"),
    )
