# CuidaMed — Supabase arquivado

**Data de exclusão:** 2026-06-29  
**Projeto Supabase ref:** `upsjjvqqjdisulingbyb`  
**Org:** MedFlow (`jneiegkmktnxwgwfynzt`)  
**Região:** sa-east-1  
**Status no momento da exclusão:** INACTIVE (pausado — plano Free, sem uso ativo)  

## Por que foi excluído
Consolidação dos projetos Supabase: apenas 2 projetos ativos no plano Free
(`atlas-b2g-medflow` e `repartition`). CuidaMed era projeto de bootcamp (Etapas 1-2 concluídas)
sem uso ativo em produção.

## Schema (migrations locais)
O schema completo está preservado em [`supabase/migrations/20260514024319_create_medicamentos_table.sql`](supabase/migrations/20260514024319_create_medicamentos_table.sql).

### Tabelas que existiam no projeto
- `medicamentos` — tabela principal (id UUID, nome, horario, doses_por_dia, app_context, created_at, updated_at)

### RLS
- RLS ON com políticas para `anon` e `authenticated`
- Todas as operações (SELECT/INSERT/UPDATE/DELETE) liberadas para `app_context = 'cuidamed'`

## Como recriar o projeto Supabase
1. Criar novo projeto em https://supabase.com/dashboard (org MedFlow ou nova)
2. Rodar o arquivo de migration acima no SQL Editor
3. Atualizar `.env` com as novas chaves (URL e anon key do novo projeto)
4. O app Python (`app.py`) continuará funcionando sem outras alterações no código

## Notas
- Nenhum dado de produção existia neste projeto (projeto de estudo/bootcamp)
- O código da aplicação continua completo neste repositório
