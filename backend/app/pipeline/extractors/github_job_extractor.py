import httpx
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class Github_job_extractor:
    def __init__(self):
        self.base_url = ""
        self.repo = ""
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": ""
        }
    #Função de busca de vagas no Github Jobs API usando cidade e estado como filtros
    async def fetch_raw_vagas(self, cidade: str, estado: str, per_page: int = 30) -> List[Dict[str, Any]]:
            local_query = f"{cidade}, {estado}"
            params = {
                 "state": "open",
                 "labels": local_query,
                 "per_page": per_page
            }
            async with httpx.AsyncClient(headers=self.headers) as client:
                try:
                    response = await client.get(self.base_url, headers=self.headers, params=params, timeout=10)
                    response.raise_for_status()
                    return response.json()
                except Exception as e:
                    logger.error(f"Erro ao buscar vagas em {self.base_url}: {e}")
                    return []
            
    @staticmethod
    def extract_company_name(body: str) -> str:
        linhas = body.split("\n")
        for linha in linhas:
            if "empresa" in linha.lower() or "company" in linha.lower():
                return linha.split(":")[-1].strip()
        return "Verificar no corpo da vaga"


    def format_jobs(self, issue: Dict[str, Any], cidade: str, estado: str) -> Dict[str, Any]:
         return {
            "titulo_cargo": issue.get("title", "Não Informado"),
            "empresa": self.extract_company_name(issue.get("body", "")),
            "cidade": cidade,
            "estado": estado,
            "requisitos": {"body_raw": issue.get("body", "")},
            "fonte": "Github_jobs",
            "url_original": issue.get("html_url", ""),
            "ativa": True  
         }

