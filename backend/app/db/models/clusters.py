from datetime import datetime
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.db.models.base import Base

class Cluster(Base):
    __tablename__ = "clusters"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    area_destino: Mapped[str] = mapped_column(String(255), nullable=False)
    regiao: Mapped[str] = mapped_column(String(100), nullable=False)
    total_pessoas: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    gerado_em: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    criado_em: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
