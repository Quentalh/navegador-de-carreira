from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.db.models.vagas import FonteVagaEnum

class VagaBase(BaseModel):
    titulo_cargo: str
    empresa: str
    cidade: str
    estado: str
    faixa_salarial_min: Optional[float] = None
    faixa_salarial_max: Optional[float] = None
    requisitos: Optional[dict] = None
    fonte: FonteVagaEnum
    url_original: str
    ativa: bool = True

class VagaCreate(VagaBase):
    hash_deduplicacao: str

class VagaResponse(VagaBase):
    id: int
    hash_deduplicacao: str
    coletada_em: datetime
    criado_em: datetime

    model_config = ConfigDict(from_attributes=True)
