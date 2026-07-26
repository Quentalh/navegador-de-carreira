import asyncio
import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Union, Optional, List, Tuple
from dotenv import load_dotenv

from .schemas.esquema_curriculo import (
    ResumeData,
    PersonalInfo,
    WorkExperience,
    Education,
    SkillSet,
    Project,
    Certification,
    ExtractionMetadata,
)
from .prompts.prompt_curriculo import SYSTEM_INSTRUCTION, RESUME_EXTRACTION_PROMPT
from .core.resiliencia import with_retry, execute_with_fallback
from .core.mascarador_pii import PIIMasker

# Carrega .env da raiz do monorepo se disponível
root_env = Path(__file__).resolve().parent.parent / ".env"
if root_env.exists():
    load_dotenv(dotenv_path=root_env)
else:
    load_dotenv()


class ResumeExtractor:
    """
    Extrator de Informações de Currículo Enterprise (Squad 3 - IA).
    Suporta chamadas síncronas/assíncronas, resiliência com retentativas,
    fallback multi-modelo (gemini-2.5-flash -> gemini-2.5-pro) e telemetria.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        primary_model: str = "gemini-2.5-flash",
        fallback_model: str = "gemini-2.5-pro",
        enable_fallback: bool = True,
    ):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.primary_model = primary_model
        self.fallback_model = fallback_model
        self.enable_fallback = enable_fallback
        self._client = None
        self._genai_lib = None

        if self.api_key and self.api_key != "cole_sua_chave_aqui":
            self._init_client()

    def _init_client(self):
        """Inicializa o cliente da API do Gemini priorizando google-genai."""
        try:
            from google import genai
            self._client = genai.Client(api_key=self.api_key)
            self._genai_lib = "google-genai"
        except ImportError:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self._client = genai
                self._genai_lib = "google-generativeai"
            except ImportError:
                self._client = None
                self._genai_lib = None

    @with_retry(max_retries=3, initial_delay=1.0)
    def _call_gemini(self, prompt: str, model_name: str) -> str:
        """Chamada resiliente e isolada à API do Gemini."""
        if not self._client:
            raise ValueError(
                "GEMINI_API_KEY não configurada ou biblioteca do Gemini não instalada. "
                "Adicione sua chave no arquivo .env ou passe como parâmetro."
            )

        if self._genai_lib == "google-genai":
            from google.genai import types
            response = self._client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    response_mime_type="application/json",
                    temperature=0.1,
                ),
            )
            return response.text
        elif self._genai_lib == "google-generativeai":
            model = self._client.GenerativeModel(
                model_name=model_name,
                system_instruction=SYSTEM_INSTRUCTION,
                generation_config={"response_mime_type": "application/json"}
            )
            response = model.generate_content(prompt)
            return response.text
        else:
            raise RuntimeError("Nenhum cliente do Gemini pôde ser inicializado.")

    def extract_from_text(self, resume_text: str, mask_pii: bool = False) -> ResumeData:
        """
        Extrai informações estruturadas de uma string contendo o texto do currículo.
        Possui resiliência, fallback multi-modelo e telemetria de latência.
        """
        start_time = time.perf_counter()
        
        target_text = resume_text
        pii_map = {}
        if mask_pii:
            target_text, pii_map = PIIMasker.mask_text(resume_text)

        prompt = RESUME_EXTRACTION_PROMPT.format(resume_text=target_text)
        used_model = self.primary_model

        def primary_attempt() -> Tuple[str, str]:
            return self._call_gemini(prompt, self.primary_model), self.primary_model

        def fallback_attempt() -> Tuple[str, str]:
            return self._call_gemini(prompt, self.fallback_model), self.fallback_model

        if self.enable_fallback:
            raw_json, used_model = execute_with_fallback(
                primary_attempt,
                fallback_attempt,
                primary_name=self.primary_model,
                fallback_name=self.fallback_model,
            )
        else:
            raw_json, used_model = primary_attempt()

        cleaned_json = self._clean_json_string(raw_json)
        
        if mask_pii and pii_map:
            cleaned_json = PIIMasker.unmask_text(cleaned_json, pii_map)

        data_dict = json.loads(cleaned_json)
        resume_data = ResumeData(**data_dict)

        # Adiciona metadados de telemetria
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        resume_data.metadata = ExtractionMetadata(
            model_used=used_model,
            latency_ms=round(elapsed_ms, 2),
            extraction_timestamp=datetime.now(timezone.utc).isoformat(),
            is_mock=False,
        )

        return resume_data

    async def extract_from_text_async(self, resume_text: str, mask_pii: bool = False) -> ResumeData:
        """
        Versão assíncrona não-bloqueante de extract_from_text.
        """
        return await asyncio.to_thread(self.extract_from_text, resume_text, mask_pii)

    def extract_from_file(self, file_path: Union[str, Path], mask_pii: bool = False) -> ResumeData:
        """
        Extrai informações estruturadas a partir de um arquivo (.txt, .md ou .pdf).
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Arquivo de currículo não encontrado: {file_path}")

        if path.suffix.lower() == ".pdf":
            text = self._read_pdf(path)
        elif path.suffix.lower() in [".txt", ".md"]:
            text = path.read_text(encoding="utf-8")
        else:
            raise ValueError(f"Formato de arquivo não suportado: {path.suffix}. Use .txt, .md ou .pdf")

        return self.extract_from_text(text, mask_pii=mask_pii)

    async def extract_from_file_async(self, file_path: Union[str, Path], mask_pii: bool = False) -> ResumeData:
        """
        Versão assíncrona de extração a partir de arquivo.
        """
        return await asyncio.to_thread(self.extract_from_file, file_path, mask_pii)

    async def extract_batch_async(
        self,
        resume_texts: List[str],
        max_concurrency: int = 3
    ) -> List[Union[ResumeData, Exception]]:
        """
        Processa múltiplos currículos simultaneamente com controle de concorrência.
        """
        semaphore = asyncio.Semaphore(max_concurrency)

        async def worker(text: str):
            async with semaphore:
                try:
                    return await self.extract_from_text_async(text)
                except Exception as e:
                    return e

        tasks = [worker(t) for t in resume_texts]
        return await asyncio.gather(*tasks)

    def mock_extract(self, resume_text: str) -> ResumeData:
        """
        Método de simulação offline para testes automatizados e validação
        da estrutura do schema sem consumo da API do Gemini.
        """
        start_time = time.perf_counter()
        lines = [line.strip() for line in resume_text.splitlines() if line.strip()]
        name = lines[0] if lines else "Candidato Simulado"
        
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', resume_text)
        email = email_match.group(0) if email_match else "candidato@example.com"
        
        phone_match = re.search(r'\(\d{2}\)\s*\d{4,5}-\d{4}', resume_text)
        phone = phone_match.group(0) if phone_match else "(11) 99999-9999"

        elapsed_ms = (time.perf_counter() - start_time) * 1000

        return ResumeData(
            personal_info=PersonalInfo(
                full_name=name,
                email=email,
                phone=phone,
                location="São Paulo, SP",
                linkedin_url="https://linkedin.com/in/candidato",
                github_url="https://github.com/candidato"
            ),
            professional_summary="Profissional da área de tecnologia com foco em desenvolvimento de software e soluções modernas.",
            seniority_level_estimate="Pleno",
            work_experiences=[
                WorkExperience(
                    company="Empresa Exemplo Tech",
                    position="Desenvolvedor de Software",
                    start_date="2021",
                    end_date="Atual",
                    is_current=True,
                    description="Atuação no desenvolvimento de APIs e aplicações web.",
                    achievements=["Melhoria de performance em 30%"],
                    technologies=["Python", "FastAPI", "React", "PostgreSQL"]
                )
            ],
            education=[
                Education(
                    institution="Universidade Exemplo",
                    degree="Bacharelado",
                    field_of_study="Ciência da Computação",
                    start_date="2017",
                    end_date="2021",
                    is_ongoing=False
                )
            ],
            skills=SkillSet(
                technical_skills=["Python", "FastAPI", "React", "Docker", "PostgreSQL"],
                soft_skills=["Trabalho em Equipe", "Comunicação", "Resolução de Problemas"],
                languages=["Português (Nativo)", "Inglês (Intermediário)"]
            ),
            projects=[
                Project(
                    name="Navegador de Carreira",
                    description="Plataforma de mapeamento de vagas e análise de currículos.",
                    technologies=["Python", "FastAPI", "React"]
                )
            ],
            certifications=[
                Certification(
                    name="Certificado de Teste AI",
                    issuing_organization="Squad 3 IA",
                    issue_date="2026"
                )
            ],
            metadata=ExtractionMetadata(
                model_used="mock-engine",
                latency_ms=round(elapsed_ms, 2),
                extraction_timestamp=datetime.now(timezone.utc).isoformat(),
                is_mock=True,
            )
        )

    def _clean_json_string(self, raw_str: str) -> str:
        """Remove marcações ```json ``` se presentes na resposta do modelo."""
        pattern = r"```(?:json)?\s*(.*?)\s*```"
        match = re.search(pattern, raw_str, re.DOTALL)
        if match:
            return match.group(1)
        return raw_str.strip()

    def _read_pdf(self, path: Path) -> str:
        """Lê o conteúdo textual de um arquivo PDF utilizando pypdf."""
        try:
            from pypdf import PdfReader
            reader = PdfReader(str(path))
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            return text
        except ImportError:
            raise ImportError(
                "A biblioteca 'pypdf' é necessária para ler arquivos PDF. "
                "Instale-a executando: pip install pypdf"
            )
