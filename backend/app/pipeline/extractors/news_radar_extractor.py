import logging
import httpx
from typing import List, Dict, Any


logger = logging.getLogger(__name__)

class News_radar_extractor:
    def __init__(self):
        self.base_url = "https://dev.to/api/articles"
        self.headers = {
            "User-Agent" : "NavegadorDeCarreira/1.0"
        }

    async def fetch_news(self, tags: str = "career", limit: int = 15) -> List[Dict[str, Any]]:

        params = {
            "tag" : tags,
            "per_page" : limit,
            "top" : 7
        }

        async with httpx.AsyncClient(headers = self.headers) as client:
            try:
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(f"Erro ao buscar notícias: {e}")
                return []
            
    def format_news(self, article: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return {
            "titulo":  article.get("title", "Sem titulo"),
            "descricao": article.get("description", ""),
            "url": article.get("url", ""),
            "fonte": "Placeholder - colocar nome da fonte, exemplo atual: 'dev.to API'",
            "tags": article.get("tag_list", []),
            "publicado_em": article.get("published_at", "")

        }
