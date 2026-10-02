# Guia de Contribuição — CuidaMed

Obrigado por contribuir com o CuidaMed! Este guia descreve o fluxo de trabalho
colaborativo adotado pela equipe, alinhado às boas práticas de desenvolvimento
em time (Issues, Branches, Pull Requests e Code Review).

## Fluxo de trabalho (passo a passo)

1. **Escolha ou crie uma Issue** descrevendo a tarefa (bug, melhoria ou nova
   funcionalidade). Toda mudança deve partir de uma Issue documentada.
2. **Crie uma branch** a partir da `master`, com nome descritivo:
   - `feature/nome-da-funcionalidade`
   - `fix/descricao-do-bug`
   - `docs/o-que-foi-documentado`
3. **Desenvolva** sua tarefa em commits pequenos e com mensagens claras
   (recomendamos o padrão [Conventional Commits](https://www.conventionalcommits.org/):
   `feat:`, `fix:`, `docs:`, `test:`, `chore:`).
4. **Garanta a qualidade localmente** antes de abrir o PR:
   ```bash
   ruff check app.py src/ tests/
   pytest tests/ -v
   ```
5. **Abra um Pull Request** para a branch `master`, vinculando a Issue com
   palavras-chave (`closes #12`, `resolves #12`).
6. **Aguarde o CI** (GitHub Actions) ficar verde — lint e testes precisam passar.
7. **Code Review:** o PR deve ser **revisado e aprovado por outro integrante** da
   equipe antes do merge. Ninguém faz merge do próprio PR sem revisão.
8. **Merge** na `master` após aprovação. O deploy é atualizado automaticamente.

## Requisitos de participação da equipe (BootCamp — Etapa 3)

- Cada integrante deve abrir **no mínimo 1 Pull Request** resolvendo uma Issue,
  implementando uma funcionalidade ou ajustando o banco de dados.
- O PR de cada aluno deve ser **revisado e aprovado (merge) por outro membro**
  do grupo, para comprovar a vivência prática de Code Review.
- Mantenha seus commits vinculados ao seu usuário do GitHub.

## Padrões de código

- Python 3.9+, seguindo o estilo verificado pelo **Ruff** (configurado em
  `pyproject.toml`, `line-length = 100`).
- Regra de negócio em `src/`, mantendo a separação entre CLI (`src/main.py`),
  interface web (`app.py`), API externa (`src/api.py`) e persistência
  (`src/medicamentos.py` / `src/supabase_repository.py`).
- Toda nova funcionalidade relevante deve vir acompanhada de **testes** em
  `tests/`.

## Configuração do ambiente

```bash
python -m venv .venv
# Windows: .\.venv\Scripts\activate   |   Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

Para usar o banco Supabase, copie `.env.example` para `.env` e preencha as
credenciais (veja o README, seção "Configuração do Supabase").

## Reportando bugs e sugestões

Abra uma Issue usando os modelos disponíveis em
`.github/ISSUE_TEMPLATE/`. Descreva o comportamento esperado, o observado e os
passos para reproduzir.
