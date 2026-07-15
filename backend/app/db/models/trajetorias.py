import enum
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Numeric
from sqlalchemy.dialects.postgresql import JSONB, ENUM
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.db.models.base import Base

class FonteDadoEnum(str, enum.Enum):
    real = "real"
    sintetico = "sintetico"

class Trajetoria(Base):
    __tablename__ = "trajetorias"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cargo_origem: Mapped[str] = mapped_column(String(255), nullable=False)
    cargo_destino: Mapped[str] = mapped_column(String(255), nullable=False)
    tempo_medio_meses: Mapped[int] = mapped_column(Integer, nullable=False)
    
    cursos_relacionados: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    faixa_investimento_medio: Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True)
    
    fonte_dado: Mapped[FonteDadoEnum] = mapped_column(ENUM(FonteDadoEnum, name="fonte_dado_enum"), nullable=False)
    
    criado_em: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
