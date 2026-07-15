import uuid
import enum
from datetime import datetime
from typing import Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.db.models.base import Base
from app.db.models.usuarios import PlanoEnum

class StatusPagamentoEnum(str, enum.Enum):
    ativo = "ativo"
    pendente = "pendente"
    cancelado = "cancelado"
    vencido = "vencido"

class Assinatura(Base):
    __tablename__ = "assinaturas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    usuario_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    plano: Mapped[PlanoEnum] = mapped_column(ENUM(PlanoEnum, name="plano_enum"), nullable=False)
    status_pagamento: Mapped[StatusPagamentoEnum] = mapped_column(ENUM(StatusPagamentoEnum, name="status_pagamento_enum"), nullable=False)
    
    iniciado_em: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    expira_em: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    criado_em: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)

    usuario: Mapped["Usuario"] = relationship(back_populates="assinaturas")
