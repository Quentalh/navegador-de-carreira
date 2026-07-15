from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from app.db.models.trajetorias import FonteDadoEnum
from app.db.models.roadmaps import StatusRoadmapEnum
from app.db.models.assinaturas import StatusPagamentoEnum
from app.db.models.usuarios import PlanoEnum

class CurriculoResponse(BaseModel):
    id: int
    usuario_id: UUID
    arquivo_url: str
    texto_extraido: Optional[str] = None
    criado_em: datetime
    model_config = ConfigDict(from_attributes=True)

class TrajetoriaResponse(BaseModel):
    id: int
    cargo_origem: str
    cargo_destino: str
    tempo_medio_meses: int
    cursos_relacionados: Optional[dict] = None
    faixa_investimento_medio: Optional[float] = None
    fonte_dado: FonteDadoEnum
    criado_em: datetime
    model_config = ConfigDict(from_attributes=True)

class RoadmapResponse(BaseModel):
    id: int
    usuario_id: UUID
    proximo_cargo_sugerido: str
    tempo_estimado_meses: int
    passos_json: Optional[dict] = None
    status: StatusRoadmapEnum
    criado_em: datetime
    atualizado_em: datetime
    model_config = ConfigDict(from_attributes=True)

class ClusterResponse(BaseModel):
    id: int
    area_destino: str
    regiao: str
    total_pessoas: int
    gerado_em: datetime
    criado_em: datetime
    model_config = ConfigDict(from_attributes=True)

class AssinaturaResponse(BaseModel):
    id: int
    usuario_id: UUID
    plano: PlanoEnum
    status_pagamento: StatusPagamentoEnum
    iniciado_em: datetime
    expira_em: Optional[datetime] = None
    criado_em: datetime
    model_config = ConfigDict(from_attributes=True)
