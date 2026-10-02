# Medication Safety Tracker: Pharmacovigilance Integration and Adverse Interaction Verification Engine

**Author:** Henri Mafra  
**License:** MIT License  
**Domain:** Medical Informatics, Pharmacovigilance, Clinical Decision Support Systems (CDSS)  

---

## 1. Overview

Medication Safety Tracker is an open-source clinical pharmacology tool designed to enhance medication adherence and verify pharmaceutical safety for elderly and polypharmacy patients. The system integrates directly with the **US Food and Drug Administration (OpenFDA)** structured database, performing real-time cross-referencing of active ingredients, contraindications, and documented Black Box Warnings.

---

## 2. Pharmacological Interaction Verification Model

Let $P = \{d_1, d_2, \dots, d_m\}$ represent the patient's active drug regimen. The interaction engine models risk over an interaction graph $\mathcal{G} = (V, E)$:

$$E_{\text{contraindicated}} = \{(d_u, d_v) \mid \text{RiskLevel}(d_u, d_v) \ge \tau_{\text{severe}}\}$$

For each ingested drug, the engine queries the OpenFDA REST endpoint:

```
GET https://api.fda.gov/drug/label.json?search=openfda.substance_name:"<SUBSTANCE>"
```

Extracted textual sections (`warnings`, `boxed_warning`, `drug_interactions`) are parsed using regular expressions and semantic entity extractors to detect adverse co-administration warnings.

---

## 3. System Architecture

- **Backend Framework:** Python 3.11, Streamlit interactive dashboard.
- **Data Schema:** Pydantic schemas validating API responses.
- **Persistence Tier:** PostgreSQL database tracking dosage adherence logs and confirmation timestamps.

---

## 4. Setup and Execution

```bash
# 1. Clone repository
git clone https://github.com/HenriMafra/medication-safety-tracker.git
cd medication-safety-tracker

# 2. Initialize virtual environment
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch application
streamlit run app.py
```

---

## 5. References

- U.S. Food and Drug Administration. (2023). *OpenFDA Drug Product Labeling API Documentation*.
- Bero, L. A. (2007). Developing Clinical Decision Support Systems for Pharmacotherapy. *Journal of the American Medical Association*.

---

## 6. License

Licensed under the MIT License. Copyright (c) Henri Mafra.
