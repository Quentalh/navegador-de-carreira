import httpx
import logging
from typing import List, Dict, Any
logger = logging.getLogger(__name__)

class Remotive_jobs_extractor:
    def __init__(self):
        self.base_url = "https://remotive.com/api/remote-jobs"
        self.headers = {"User-Agent": "NavegadorDeCarreira/1.0"}

    async def fetch_jobs(self, categoria: str = "software-development", limit: int = 30) -> List[Dict[str, Any]]:
        params = {"category": categoria}
        async with httpx.AsyncClient(headers=self.headers) as client:
            try:
                response = await client.get(self.base_url, params=params, timeout=15)
                response.raise_for_status()
                data = response.json()
                return data.get("jobs", [])[:limit] # Removido filtro rígido para garantir retorno
            except Exception as e:
                logger.error(f"Erro ao buscar vagas Remotive: {e}")
                return []

    def format_jobs(self, job: Dict[str, Any]) -> Dict[str, Any]:
        location = job.get("candidate_required_location", "")

        return{
            
            "titulo_cargo": job.get("title", "Não Informado"),
            "empresa": job.get("company_name", "Não Informado"),
            "cidade": location,
            "estado": "Não utilizado por vagas remotas internacionais",
            "requisitos": {"body_raw": job.get("description", "")},
            "fonte": "Remotive",
            "url_original": job.get("url", ""),
            "ativa": True
        }