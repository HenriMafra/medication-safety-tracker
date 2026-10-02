# 💊 Medication Safety Tracker — Gerenciador de Adesão & Validador de Interações com OpenFDA

Aplicação web e CLI para controle de rotina medicamentosa voltada a idosos e cuidadores, combinando agendamento dinâmico de doses com **motor de verificação de segurança farmacológica e advertências de bula integrado à API oficial da Food and Drug Administration (OpenFDA)**.

---

## 📌 Que Problema Resolve?

A polifarmácia (uso simultâneo de múltiplos medicamentos) é uma das principais causas de internações evitáveis em idosos. Erros comuns incluem:
- Esquecimento ou duplicidade de doses.
- Ingestão conjunta de fármacos com interações perigosas (ex: anti-inflamatórios combinados com anticoagulantes).
- Desconhecimento de advertências críticas de bula (Black Box Warnings).

O **Medication Safety Tracker** resolve esses riscos fornecendo:
1. Agenda visual de horários com confirmação de tomada e lembretes para cuidadores.
2. Consulta em tempo real à base de dados estruturada do OpenFDA para extração automática de princípios ativos, contraindicações e efeitos adversos documentados.
3. Interface acessível de alto contraste, com suporte a familiares supervisionarem remotamente o tratamento.

---

## ⚙️ Diferencial Técnico & Integração OpenFDA

- **Consulta Estruturada OpenFDA REST:**
  Integração direta aos endpoints `api.fda.gov/drug/label.json`, realizando parsing inteligente de campos de texto livre (`warnings`, `drug_interactions`, `boxed_warning`).
- **Resiliência Offline-First:**
  Suporte a cache local em SQLite/PostgreSQL para garantir que os horários de medicação continuem disponíveis mesmo em caso de instabilidade na conexão com a internet.

---

## 🏗️ Stack Tecnológica

- **Backend & Interface:** Python 3.11+, Streamlit (Dashboard interativo responsivo).
- **Banco de Dados:** PostgreSQL / Supabase para sincronização em nuvem e persistência de adesão.
- **Bibliotecas:** `requests`, `pandas`, `pydantic` para validação estrita de schemas de resposta.

---

## 🚀 Como Executar Localmente

```bash
# 1. Clone o repositório
git clone https://github.com/HenriMafra/medication-safety-tracker.git
cd medication-safety-tracker

# 2. Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: .\venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Inicie o dashboard
streamlit run app.py
```

---

## 📄 Licença

Distribuído sob a licença **MIT**. Desenvolvido por **Henri Mafra**.
