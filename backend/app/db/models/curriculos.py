import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.db.models.base import Base

class Curriculo(Base):
    __tablename__ = "curriculos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    usuario_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    arquivo_url: Mapped[str] = mapped_column(String(500), nullable=False)
    texto_extraido: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    criado_em: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)

    usuario: Mapped["Usuario"] = relationship(back_populates="curriculos")
