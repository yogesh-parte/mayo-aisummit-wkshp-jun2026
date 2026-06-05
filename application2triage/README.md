# Colorectal Cancer Intelligent Triage System (Nanopublication + FHIR RDF)

This package contains a complete, runnable local demo of an **explainable, provenance-aware colorectal cancer patient triage system** built with:

- **Nanopublications** (fine-grained, citable scientific assertions)
- **PROV-O provenance** (full audit trail)
- **FHIR RDF** patient data
- **rdflib** (pure local Python, no database required)

## What It Does

Given a patient’s FHIR data, the system automatically:
1. Detects cancer type (Rectal vs Colon)
2. Checks metastatic status
3. Checks MSI/MMR status
4. Checks for emergency/obstructing presentation
5. Returns the correct triage pathway + importance level
6. Provides full provenance (which guideline the rule came from)

---

## Step-by-Step Instructions to Run

### 1. Prerequisites

- Python 3.9+
- `pip` package manager

### 2. Setup Environment

```bash
cd application2triage
python -m venv venv
source venv/bin/activate          # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the Demo

```bash
python colorectal_triage_agent.py
```

You should see output similar to:

```
Loaded: data/nanopubs/colorectal_framework.np.trig
...
Total triples loaded: XXXX

=== Triage Recommendation for PATIENT-12345 ===
{
  "patientId": "PATIENT-12345",
  "cancerType": "Rectal",
  ...
  "recommendedPathway": "Multidisciplinary evaluation (MedOnc, RadOnc, SurgOnc)",
  ...
}
```

---

## Project Structure

```
application2triage/
├── README.md
├── requirements.txt
├── colorectal_triage_agent.py          # Main agent (rdflib only)
├── data/
│   ├── nanopubs/
│   │   ├── colorectal_framework.np.trig
│   │   ├── rectal_vs_colon.np.trig
│   │   ├── metastatic_vs_non.np.trig
│   │   ├── mmr_msi.np.trig
│   │   └── obstructing_emergency.np.trig
│   └── patient-example-12345.ttl       # Sample FHIR RDF patient
└── run_demo.sh                         # (optional) helper script
```

---

## How to Customize

### Change Patient Data
Edit `data/patient-example-12345.ttl` or create new `.ttl` files following the same FHIR RDF structure.

### Add New Decision Rules
1. Create a new `.trig` nanopublication file in `data/nanopubs/`
2. Follow the existing structure (Head + Assertion + Provenance + PubInfo)
3. Re-run the script — it will automatically pick up new files.

### Extend the Agent
Edit `colorectal_triage_agent.py` and add new methods or improve the SPARQL logic.

---

## Key Technologies Used

- **Nanopublications** – Fine-grained, citable scientific claims
- **PROV-O** – Rich provenance for trust and auditability
- **FHIR RDF** – Standard healthcare data representation
- **rdflib** – Pure Python RDF library (no external database needed)
- **SPARQL** – Powerful querying over the combined knowledge graph

---

## Next Steps / Production Ideas

- Replace local rdflib with **GraphDB** or **Stardog** for scale
- Add **SHACL** validation shapes
- Integrate with **LangGraph** or **CrewAI** multi-agent orchestration
- Connect to real EHR via FHIR API
- Add **Streamlit/Gradio** web UI
- Publish nanopublications to Knowledge Pixels registry

---

**Author**: Built for leadership demonstration of provenance-aware, explainable clinical decision support.

**License**: MIT (for demo purposes)

---

For questions or extensions, refer to the conversation history or contact the developer.
