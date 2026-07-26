from typing import List, Optional
from pydantic import BaseModel, Field


class PersonalInfo(BaseModel):
    full_name: str = Field(..., description="Nome completo do candidato")
    email: Optional[str] = Field(None, description="Endereço de e-mail de contato")
    phone: Optional[str] = Field(None, description="Telefone de contato com DDD")
    location: Optional[str] = Field(None, description="Cidade, Estado ou País de residência")
    linkedin_url: Optional[str] = Field(None, description="URL do perfil no LinkedIn")
    github_url: Optional[str] = Field(None, description="URL do perfil no GitHub")
    portfolio_url: Optional[str] = Field(None, description="URL do site/portfólio pessoal")


class WorkExperience(BaseModel):
    company: str = Field(..., description="Nome da empresa ou organização")
    position: str = Field(..., description="Cargo ou título da posição ocupada")
    location: Optional[str] = Field(None, description="Localização da empresa (ex: São Paulo - SP, Remoto)")
    start_date: Optional[str] = Field(None, description="Data de início (ex: MM/AAAA ou AAAA)")
    end_date: Optional[str] = Field(None, description="Data de término (ex: MM/AAAA, AAAA ou 'Atual')")
    is_current: bool = Field(False, description="Indica se é o emprego atual do candidato")
    description: Optional[str] = Field(None, description="Resumo das responsabilidades exercidas")
    achievements: List[str] = Field(default_factory=list, description="Lista de conquistas ou destaques quantificáveis")
    technologies: List[str] = Field(default_factory=list, description="Linguagens, frameworks e ferramentas utilizadas")


class Education(BaseModel):
    institution: str = Field(..., description="Nome da instituição de ensino")
    degree: Optional[str] = Field(None, description="Grau acadêmico (ex: Bacharelado, Tecnólogo, Pós-graduação, Ensino Médio)")
    field_of_study: Optional[str] = Field(None, description="Área de estudo ou curso (ex: Ciência da Computação, Engenharia de Software)")
    start_date: Optional[str] = Field(None, description="Data de início")
    end_date: Optional[str] = Field(None, description="Data de conclusão ou previsão de término")
    is_ongoing: bool = Field(False, description="Indica se o curso ainda está em andamento")



class SkillSet(BaseModel):
    technical_skills: List[str] = Field(default_factory=list, description="Habilidades técnicas (ex: Python, Docker, PostgreSQL, React)")
    soft_skills: List[str] = Field(default_factory=list, description="Habilidades comportamentais (ex: Liderança, Comunicação, Trabalho em equipe)")
    languages: List[str] = Field(default_factory=list, description="Idiomas falados e nível de fluência (ex: Português Nativo, Inglês Avançado)")


class Project(BaseModel):
    name: str = Field(..., description="Nome do projeto")
    description: Optional[str] = Field(None, description="Descrição detalhada do projeto e objetivo")
    repository_url: Optional[str] = Field(None, description="Link do código fonte no GitHub/GitLab")
    live_url: Optional[str] = Field(None, description="Link do projeto em produção ou demonstração")
    technologies: List[str] = Field(default_factory=list, description="Tecnologias principais utilizadas no projeto")


class Certification(BaseModel):
    name: str = Field(..., description="Nome do certificado ou curso livre")
    issuing_organization: Optional[str] = Field(None, description="Instituição ou plataforma emissora (ex: AWS, Coursera, Alura)")
    issue_date: Optional[str] = Field(None, description="Data de emissão (ex: 2024)")
    credential_url: Optional[str] = Field(None, description="Link de validação do certificado")


class ExtractionMetadata(BaseModel):
    model_used: Optional[str] = Field(None, description="Modelo de IA utilizado na extração (ex: gemini-2.5-flash)")
    latency_ms: Optional[float] = Field(None, description="Tempo de processamento da extração em milissegundos")
    extraction_timestamp: Optional[str] = Field(None, description="Timestamp ISO da extração")
    is_mock: bool = Field(False, description="Indica se a resposta veio de simulação offline")


class ResumeData(BaseModel):
    """
    Modelo consolidado de dados extraídos do currículo.
    Serve como contrato JSON entre o serviço de IA e a API do backend.
    """
    personal_info: PersonalInfo = Field(..., description="Informações pessoais e de contato")
    professional_summary: Optional[str] = Field(None, description="Resumo profissional ou objetivo de carreira extraído")
    seniority_level_estimate: Optional[str] = Field(
        None, description="Estimativa de nível de senioridade (ex: Estagiário, Júnior, Pleno, Sênior, Especialista, Lead)"
    )
    work_experiences: List[WorkExperience] = Field(default_factory=list, description="Histórico de experiências profissionais")
    education: List[Education] = Field(default_factory=list, description="Histórico de formação acadêmica")
    skills: SkillSet = Field(default_factory=SkillSet, description="Conjunto de habilidades e idiomas")
    projects: List[Project] = Field(default_factory=list, description="Projetos relevantes listados no currículo")
    certifications: List[Certification] = Field(default_factory=list, description="Certificações e cursos extracurriculares")
    metadata: Optional[ExtractionMetadata] = Field(None, description="Metadados de telemetria da extração")

