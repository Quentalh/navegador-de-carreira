# 🤖 Squad 3 - Inteligência Artificial & Prompt Engineering (Senior Lead Architecture)

Bem-vindo ao módulo de IA da **Squad 3** do projeto **Navegador de Carreira**. Este módulo é uma arquitetura de serviço de IA pronta para produção enterprise, responsável pela extração, resiliência e estruturação de currículos profissionais através da API do **Google Gemini**.

---

## 📁 Estrutura de Pastas (`/ai`)

```
/ai
├── README.md                   # Documentação da Squad 3 e Guia de Integração
├── requirements.txt            # Dependências Python específicas do módulo de IA
├── extractor.py                # Extrator Enterprise (ResumeExtractor - Sync/Async)
├── router.py                   # Blueprint de Rota FastAPI para a Squad 4
├── test_resume_extractor.py    # Suite de testes e benchmark de extração
├── core/
│   ├── __init__.py
│   ├── resilience.py           # Retry com Backoff Exponencial + Fallback Multi-Modelo
│   └── pii_masker.py           # Mascaramento de dados sensíveis (LGPD / PII)
├── schemas/
│   ├── __init__.py
│   └── resume_schema.py        # Modelos Pydantic (Contrato de Dados JSON & Telemetria)
├── prompts/
│   ├── __init__.py
│   └── resume_prompt.py        # System Instruction e Engenharia de Prompt
└── sample_resumes/             # Currículos de teste (.txt / .pdf)
    ├── sample_dev.txt
    └── sample_junior.txt
```

---

## 🚀 Recursos de Nível Senior Lead

1. **⚡ Suporte Assíncrono (`async/await`) & Batching:**
   - Métodos `extract_from_text_async` e `extract_from_file_async` para não bloquear o event loop da API.
   - `extract_batch_async` para processar múltiplos currículos em paralelo com controle de concorrência.

2. **🛡️ Resiliência & Cascata Multi-Modelo:**
   - Decorador `@with_retry` com **Exponential Backoff e Jitter** para tratar limites de cota (`429`) ou falhas temporárias.
   - **Fallback Automático:** Tenta primeiro o modelo `gemini-2.5-flash`. Em caso de erro de validação ou indisponibilidade, migra automaticamente para o `gemini-2.5-pro`.

3. **🔒 Mascaramento de Dados Sensíveis (LGPD / PII Masking):**
   - Parâmetro `mask_pii=True` para anonimizar e-mails, telefones e CPFs antes de enviar à LLM ou salvar em logs.

4. **📊 Telemetria e Métricas:**
   - Todo JSON retornado contém um objeto `metadata` informando a latência em ms, o modelo exato utilizado e o timestamp ISO da extração.

---

## 🛠️ Como Executar e Testar

### 1. Instalar as Dependências
```bash
pip install -r ai/requirements.txt
```

### 2. Configurar a Chave no `.env`
No arquivo `.env` na raiz do projeto:
```env
GEMINI_API_KEY=sua_chave_do_gemini_aqui
```

### 3. Rodar os Testes de Extração

#### 🧪 Modo Simulação (Offline / Mock)
```bash
python ai/test_resume_extractor.py --mock
```

#### ⚡ Modo Real (Gemini API com Telemetria)
```bash
python ai/test_resume_extractor.py
```

#### 🔒 Modo Real com Mascaramento LGPD
```bash
python ai/test_resume_extractor.py --pii
```

---

## 🔌 Guia para Squad 4 (Backend API) Integrar

A Squad 4 pode conectar a IA à API FastAPI principal (`/backend/main.py`) em **apenas 2 linhas de código**:

```python
from fastapi import FastAPI
from ai.router import router as ai_router

app = FastAPI(title="Navegador de Carreira API")

# Monta automaticamente as rotas da Squad 3 (/ai/extract-text e /ai/extract-file)
app.include_router(ai_router)
```

### Rotas Disponíveis no Swagger OpenAPI:
- `POST /ai/extract-text`: Envia JSON `{ "resume_text": "...", "mask_pii": false }`
- `POST /ai/extract-file`: Upload multipart de arquivos `.pdf`, `.txt` ou `.md`.
