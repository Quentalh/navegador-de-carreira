"""
FastAPI Router Blueprint para a Squad 3 (Módulo de IA).
Permite que a Squad 4 (Backend) exponha os endpoints de extração de currículos com facilidade.
"""
from pathlib import Path
from typing import Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, status
from pydantic import BaseModel

from .extrator import ResumeExtractor
from .schemas.esquema_curriculo import ResumeData

router = APIRouter(prefix="/ia", tags=["IA Extração de Currículos"])
extractor = ResumeExtractor()


class TextExtractRequest(BaseModel):
    resume_text: str
    mask_pii: bool = False


@router.post(
    "/extrair-texto",
    response_model=ResumeData,
    summary="Extrai dados estruturados a partir do texto do currículo",
    status_code=status.HTTP_200_OK,
)
async def extract_resume_from_text(payload: TextExtractRequest):
    """
    Recebe o texto bruto do currículo e retorna um JSON padronizado com
    dados de contato, experiências, formação, habilidades e senioridade estimada.
    """
    if not payload.resume_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O texto do currículo não pode estar vazio."
        )

    try:
        if not extractor.api_key or extractor.api_key == "cole_sua_chave_aqui":
            return extractor.mock_extract(payload.resume_text)
        return await extractor.extract_from_text_async(payload.resume_text, mask_pii=payload.mask_pii)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Falha ao processar o currículo via Gemini AI: {str(e)}"
        )


@router.post(
    "/extrair-arquivo",
    response_model=ResumeData,
    summary="Extrai dados estruturados a partir do upload de arquivo (PDF/TXT)",
    status_code=status.HTTP_200_OK,
)
async def extract_resume_from_file(
    file: UploadFile = File(...),
    mask_pii: bool = Form(False),
):
    """
    Recebe um arquivo de currículo (PDF, TXT ou Markdown) e retorna o JSON estruturado.
    """
    filename = file.filename or "curriculo.txt"
    extension = Path(filename).suffix.lower()

    if extension not in [".pdf", ".txt", ".md"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Formato '{extension}' não suportado. Envie um arquivo .pdf, .txt ou .md."
        )

    try:
        content = await file.read()
        if extension == ".pdf":
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(content)
                tmp_path = tmp.name

            try:
                if not extractor.api_key or extractor.api_key == "cole_sua_chave_aqui":
                    return extractor.mock_extract(content.decode("utf-8", errors="ignore"))
                return await extractor.extract_from_file_async(tmp_path, mask_pii=mask_pii)
            finally:
                Path(tmp_path).unlink(missing_ok=True)
        else:
            text = content.decode("utf-8", errors="ignore")
            if not extractor.api_key or extractor.api_key == "cole_sua_chave_aqui":
                return extractor.mock_extract(text)
            return await extractor.extract_from_text_async(text, mask_pii=mask_pii)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Falha no processamento do arquivo de currículo: {str(e)}"
        )
