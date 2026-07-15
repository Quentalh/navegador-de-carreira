# Database Schema - Navegador de Carreira

Este documento descreve o modelo relacional do projeto, implementado em PostgreSQL via SQLAlchemy.

## Diagrama Entidade-Relacionamento (ERD)

```mermaid
erDiagram
    USUARIOS {
        uuid id PK
        varchar nome
        varchar email UK "Indexado"
        varchar senha_hash
        numeric disponibilidade_financeira_mensal "Nullable"
        varchar cidade "Nullable"
        varchar estado "Nullable"
        float latitude "Nullable"
        float longitude "Nullable"
        jsonb perfil_estruturado_json "Nullable"
        enum plano "free/premium"
        timestamp criado_em
        timestamp atualizado_em
    }

    CURRICULOS {
        int id PK
        uuid usuario_id FK "Cascade Delete, Indexado"
        varchar arquivo_url
        text texto_extraido "Nullable"
        timestamp criado_em
    }

    VAGAS {
        int id PK
        varchar titulo_cargo
        varchar empresa
        varchar cidade
        varchar estado
        numeric faixa_salarial_min "Nullable"
        numeric faixa_salarial_max "Nullable"
        jsonb requisitos "Nullable"
        enum fonte "linkedin/glassdoor/outro"
        varchar url_original UK "Indexado"
        varchar hash_deduplicacao "Indexado"
        boolean ativa "Default True"
        timestamp coletada_em
        timestamp criado_em
    }

    TRAJETORIAS {
        int id PK
        varchar cargo_origem
        varchar cargo_destino
        int tempo_medio_meses
        jsonb cursos_relacionados "Nullable"
        numeric faixa_investimento_medio "Nullable"
        enum fonte_dado "real/sintetico"
        timestamp criado_em
    }

    ROADMAPS {
        int id PK
        uuid usuario_id FK "Cascade Delete, Indexado"
        varchar proximo_cargo_sugerido
        int tempo_estimado_meses
        jsonb passos_json "Nullable"
        enum status "gerando/pronto/erro"
        timestamp criado_em
        timestamp atualizado_em
    }

    ROADMAP_VAGAS {
        int roadmap_id PK, FK "Cascade Delete"
        int vaga_id PK, FK "Cascade Delete"
    }

    CLUSTERS {
        int id PK
        varchar area_destino
        varchar regiao
        int total_pessoas "Default 0"
        timestamp gerado_em
        timestamp criado_em
    }

    ASSINATURAS {
        int id PK
        uuid usuario_id FK "Cascade Delete, Indexado"
        enum plano "free/premium"
        enum status_pagamento "ativo/pendente/cancelado/vencido"
        timestamp iniciado_em
        timestamp expira_em "Nullable"
        timestamp criado_em
    }

    USUARIOS ||--o{ CURRICULOS : "possui"
    USUARIOS ||--o{ ROADMAPS : "possui"
    USUARIOS ||--o{ ASSINATURAS : "possui"
    
    ROADMAPS ||--o{ ROADMAP_VAGAS : "relaciona"
    VAGAS ||--o{ ROADMAP_VAGAS : "referencia"
```

## Notas Importantes:
- **`CLUSTERS`** é um agregado B2B estritamente anonimizado. Sem *Foreign Keys* ou referências para a tabela `USUARIOS`.
- Os índices na tabela de `VAGAS` otimizam as buscas compostas por cidade + cargo.
- Deleções em cascata foram configuradas para garantir limpeza de dados ao excluir um usuário.
