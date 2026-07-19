import asyncio
import logging
from github_job_extractor import Github_job_extractor
from remotive_API_job_extractor import Remotive_jobs_extractor
from news_radar_extractor import News_radar_extractor

logger = logging.getLogger(__name__)

class JobOrchestrator:
    def __init__(self):
        self.github_extractor = Github_job_extractor()
        self.remotive_extractor = Remotive_jobs_extractor()
        self.news_extractor = News_radar_extractor()

    async def run_all(self):
            print("Iniciando coleta de dados...")
            results = await asyncio.gather(
                self.github_extractor.fetch_jobs("Remoto", ""),
                self.remotive_extractor.fetch_jobs("software-development", limit=10),
                self.news_extractor.fetch_news(tags="career", limit=5),
                return_exceptions=True
            )
            
            # Debug
            for i, res in enumerate(results):
                fonte = ["GitHub", "Remotive", "Notícias"][i]
                if isinstance(res, Exception):
                    print(f"Erro em {fonte}: {res}")
                else:
                    print(f"Sucesso em {fonte}: {len(res)} itens encontrados.")

if __name__ == "__main__":
    orchestrator = JobOrchestrator()
    asyncio.run(orchestrator.run_all())
