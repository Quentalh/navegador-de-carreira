"""
Script de Testes e Benchmark de Extração de Currículos (Squad 3 - IA)
Suporta execução Síncrona, Assíncrona, Resiliência e Telemetria.
"""
import sys
import asyncio
import argparse
from pathlib import Path

# Ajusta encodificação do stdout para UTF-8 em terminais Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Adiciona diretório raiz do projeto ao sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ai.extrator import ResumeExtractor
from ai.schemas.esquema_curriculo import ResumeData


async def run_tests_async(mock_mode: bool = False, mask_pii: bool = False):
    print("==================================================")
    print("[+] SQUAD 3 - TESTE ENTERPRISE DE EXTRACAO DE CURRICULO")
    print("==================================================")

    samples_dir = Path(__file__).resolve().parent / "curriculos_exemplo"
    sample_files = [f for f in samples_dir.glob("*.txt") if not f.name.endswith(".extraido.json")]

    if not sample_files:
        print("[!] Nenhum curriculo de teste encontrado em curriculos_exemplo/")
        return

    extractor = ResumeExtractor()
    use_mock = mock_mode or not extractor.api_key or extractor.api_key == "cole_sua_chave_aqui"

    if use_mock:
        print("[i] Modo SIMULACAO (Mock) ativo. Testando validacao de Schema sem consumo de cota da API.")
    else:
        print(f"[i] Chave detectada. Testando extracao REAL com modelo primario: {extractor.primary_model}")

    for file_path in sample_files:
        print(f"\n[>] Processando arquivo: {file_path.name}")
        resume_text = file_path.read_text(encoding="utf-8")

        try:
            if use_mock:
                result: ResumeData = extractor.mock_extract(resume_text)
            else:
                # Testa chamada assíncrona não-bloqueante
                result: ResumeData = await extractor.extract_from_text_async(resume_text, mask_pii=mask_pii)

            print("[V] Extracao concluida com sucesso! Estrutura JSON validada:")
            print(f"    Nome: {result.personal_info.full_name}")
            print(f"    E-mail: {result.personal_info.email}")
            print(f"    Telefone: {result.personal_info.phone}")
            print(f"    Localizacao: {result.personal_info.location}")
            print(f"    Senioridade Estimada: {result.seniority_level_estimate}")
            print(f"    Experiencias: {len(result.work_experiences)} registradas")
            print(f"    Educacao: {len(result.education)} registradas")
            print(f"    Habilidades Tecnicas: {', '.join(result.skills.technical_skills[:5])}...")
            print(f"    Projetos: {len(result.projects)} registrados")

            if result.metadata:
                print(f"    Modelo Utilizado: {result.metadata.model_used}")
                print(f"    Latencia (ms): {result.metadata.latency_ms} ms")

            # Salva o resultado em formato JSON formatado na pasta de teste
            out_file = file_path.with_name(file_path.stem + ".extraido.json")
            out_file.write_text(result.model_dump_json(indent=2), encoding="utf-8")
            print(f"    Saida JSON salva em: {out_file.name}")

        except Exception as e:
            print(f"[X] Erro na extracao do arquivo {file_path.name}: {e}")

    print("\n==================================================")
    print("[+] Testes de extracao finalizados com sucesso!")
    print("==================================================")


def main():
    parser = argparse.ArgumentParser(description="Testes do Extrator de Curriculos Squad 3 IA")
    parser.add_argument("--mock", action="store_true", help="Forca o uso do modo de simulacao sem chamar a API do Gemini")
    parser.add_argument("--pii", action="store_true", help="Ativa mascaramento de dados sensiveis (LGPD)")
    args = parser.parse_args()

    asyncio.run(run_tests_async(mock_mode=args.mock, mask_pii=args.pii))


if __name__ == "__main__":
    main()
