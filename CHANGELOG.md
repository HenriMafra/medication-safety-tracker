# Changelog

## [Não lançado]

### Adicionado
- Arquivo `LICENSE` (MIT) e seção de licença no README
- `CONTRIBUTING.md` com o fluxo colaborativo (Issues, Branches, PRs e Code Review)
- Modelos de Issue (`bug_report`, `feature_request`) e de Pull Request em `.github/`
- `.env.example` documentando as variáveis do Supabase
- Tabela de integrantes (com matrícula) e exemplo de uso (CLI) no README

## [2.0.0] - 2026-05-14

### Adicionado
- Persistencia em banco de dados Supabase/PostgreSQL
- Migracao SQL para criar a tabela `medicamentos` com RLS e politicas de acesso
- Camada `supabase_repository.py` para isolar comunicacao com o banco
- Funcionalidade de atualizacao de medicamentos na CLI e na interface web
- Testes automatizados para o fluxo de armazenamento Supabase com mock

### Alterado
- Interface Streamlit passou a usar a regra de negocio central do projeto
- README atualizado com instrucoes de Supabase, deploy, lint e testes

## [1.1.0] - 2026-03-16

### Adicionado
- Integracao com API publica OpenFDA para consulta de informacoes de medicamentos
- Interface web via Streamlit (app.py) com suporte a deploy em nuvem
- Teste de integracao (tests/test_integracao.py) validando comunicacao com API externa
- Nova opcao no menu CLI: "5. Consultar informacoes do medicamento (API)"
- Dependencias: requests, streamlit

## [1.0.0] - 2026-03-09

### Adicionado
- Interface CLI com menu interativo
- Funcionalidades: adicionar, listar, remover e buscar medicamentos
- Persistencia de dados em arquivo JSON local
- Testes automatizados com pytest
- Linting com ruff
- Pipeline de CI com GitHub Actions
