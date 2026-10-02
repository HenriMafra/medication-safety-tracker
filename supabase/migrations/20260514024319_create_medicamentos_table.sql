create extension if not exists pgcrypto;

create table if not exists public.medicamentos (
  id uuid primary key default gen_random_uuid(),
  nome text not null check (length(trim(nome)) > 0),
  horario time not null,
  doses_por_dia integer not null check (doses_por_dia > 0),
  app_context text not null default 'cuidamed' check (app_context = 'cuidamed'),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

alter table public.medicamentos
  add column if not exists app_context text not null default 'cuidamed'
  check (app_context = 'cuidamed');

create index if not exists idx_medicamentos_nome
  on public.medicamentos using btree (lower(nome));

create or replace function public.set_updated_at()
returns trigger
language plpgsql
set search_path = public
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists set_medicamentos_updated_at on public.medicamentos;

create trigger set_medicamentos_updated_at
before update on public.medicamentos
for each row
execute function public.set_updated_at();

alter table public.medicamentos enable row level security;

grant select, insert, update, delete on table public.medicamentos to anon, authenticated;

drop policy if exists "Medicamentos podem ser lidos pela aplicacao" on public.medicamentos;
drop policy if exists "Medicamentos podem ser criados pela aplicacao" on public.medicamentos;
drop policy if exists "Medicamentos podem ser atualizados pela aplicacao" on public.medicamentos;
drop policy if exists "Medicamentos podem ser removidos pela aplicacao" on public.medicamentos;

create policy "Medicamentos podem ser lidos pela aplicacao"
on public.medicamentos
for select
to anon, authenticated
using (app_context = 'cuidamed');

create policy "Medicamentos podem ser criados pela aplicacao"
on public.medicamentos
for insert
to anon, authenticated
with check (app_context = 'cuidamed');

create policy "Medicamentos podem ser atualizados pela aplicacao"
on public.medicamentos
for update
to anon, authenticated
using (app_context = 'cuidamed')
with check (app_context = 'cuidamed');

create policy "Medicamentos podem ser removidos pela aplicacao"
on public.medicamentos
for delete
to anon, authenticated
using (app_context = 'cuidamed');
