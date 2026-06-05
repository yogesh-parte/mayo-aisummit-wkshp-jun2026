# Colorectal Cancer Triage Knowledge Package

This package contains structured knowledge artifacts for colorectal cancer patient triage using Nanopublications and RDF.

## Contents

1. `original_text.txt` - The source checklist text
2. `single_nanopub/` - Single enriched nanopublication + queries
3. `separate_nanopubs/` - Granular nanopublications (best practice) + queries

## How to Use

### Option 1: Single Nanopublication (simpler)
```bash
cd single_nanopub
python query_single.py
```

### Option 2: Separate Nanopublications (recommended for Linked Data)
```bash
cd separate_nanopubs
python query_separate.py
```

Use any RDF tool (GraphDB, rdflib, Apache Jena) to load the .trig files.

## Project Purpose
- Machine-actionable triage rules with full provenance
- Ready for AI agents, clinical decision support, and knowledge graphs

Generated on: 2026-06-04
