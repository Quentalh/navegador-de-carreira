from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.db.models.usuarios import PlanoEnum

class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    disponibilidade_financeira_mensal: Optional[float] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    perfil_estruturado_json: Optional[dict] = None
    plano: PlanoEnum = PlanoEnum.free

class UsuarioCreate(UsuarioBase):
    senha: str

class UsuarioResponse(UsuarioBase):
    id: UUID
    criado_em: datetime
    atualizado_em: datetime

    model_config = ConfigDict(from_attributes=True)
