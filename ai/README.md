# 🤖 Squad 3 - Inteligência Artificial & Prompt Engineering

Bem-vindo ao módulo de IA da **Squad 3** do projeto **Navegador de Carreira**. Este módulo é responsável pela extração, resiliência e estruturação de currículos profissionais em JSON através da API do **Google Gemini**.

---

## 📁 Estrutura de Pastas (`/ai`)

```
/ai
├── README.md                   # Documentação da Squad 3 e Guia de Integração
├── requirements.txt            # Dependências Python específicas do módulo de IA
├── extrator.py                 # Extrator Principal (ResumeExtractor - Sync/Async)
├── rotas.py                    # Blueprint de Rotas FastAPI para a Squad 4
├── testar_extrator.py          # Script de testes e benchmark de extração
├── core/
│   ├── __init__.py
│   ├── resiliencia.py          # Retry com Backoff Exponencial + Fallback Multi-Modelo
│   └── mascarador_pii.py       # Mascaramento de dados sensíveis (LGPD / PII)
├── schemas/
│   ├── __init__.py
│   └── esquema_curriculo.py    # Modelos Pydantic (Contrato de Dados JSON & Telemetria)
├── prompts/
│   ├── __init__.py
│   └── prompt_curriculo.py     # System Instruction e Engenharia de Prompt
└── curriculos_exemplo/         # Currículos de teste (.txt / .pdf)
    ├── exemplo_dev.txt
    └── exemplo_junior.txt
```

---

## 🛠️ Como Executar os Testes

```bash
# Teste Offline (Simulação / Mock)
python ai/testar_extrator.py --mock

# Teste Real (Gemini API com Telemetria)
python ai/testar_extrator.py
```

---

## 🔌 Guia para Squad 4 (Backend API) Integrar

A Squad 4 pode conectar as rotas de IA à API FastAPI principal (`/backend/main.py`):

```python
from fastapi import FastAPI
from ai.rotas import router as ia_router

app = FastAPI(title="Navegador de Carreira API")

# Monta as rotas da Squad 3 (/ia/extrair-texto e /ia/extrair-arquivo)
app.include_router(ia_router)
```
