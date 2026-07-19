from pydantic import BaseModel, ConfigDict, model_validator
from typing import Optional
from datetime import datetime
from app.db.models.vagas import FonteVagaEnum

class VagaBase(BaseModel):
    titulo_cargo: str
    empresa: str
    cidade: Optional[str] = None
    estado: Optional[str] = None
    localizacao: Optional[str] = None
    faixa_salarial_min: Optional[float] = None
    faixa_salarial_max: Optional[float] = None
    requisitos: Optional[dict] = None
    fonte: FonteVagaEnum
    url_original: str
    ativa: bool = True

    @model_validator(mode="before")
    @classmethod
    #Função placeholder para tratar casos onde a localização é enviada como um dict (ex: "localizacao" : "Recife, Pe")
    def tratar_localizacao(cls, data: dict) -> dict:
        local = data.get("localizacao")
        if local and (not data.get("cidade") or not data.get("estado")):
            if "," or " - " in local:
                if "," in local:
                    parts = local.split(",")
                    data["cidade"] = parts[0].strip()
                    data["estado"] = parts[1].strip() if len(parts) > 1
                elif " - " in local:
                    parts = local.split(" - ")
                    data["cidade"] = parts[0].strip()
                    data["estado"] = parts[1].strip() if len(parts) > 1
                else:
                    data["cidade"] = local.strip()
                    data["estado"] = "Não informado"
        if not data.get("cidade") and not data.get("estado"):
            data("cidade") = "Não informado"
            data("estado") = "Não informado"
        return data

            
class VagaCreate(VagaBase):
    hash_deduplicacao: str

class VagaResponse(VagaBase):
    id: int
    hash_deduplicacao: str
    coletada_em: datetime
    criado_em: datetime

    model_config = ConfigDict(from_attributes=True)
