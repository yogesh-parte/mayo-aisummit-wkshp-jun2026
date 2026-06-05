from rdflib import Graph
import json

g = Graph()
files = ["colorectal_framework.np.trig", "rectal_vs_colon.np.trig", "metastatic_vs_non.np.trig", "mmr_msi.np.trig", "obstructing_emergency.np.trig"]

for f in files:
    try:
        g.parse(f, format="trig")
    except:
        pass  # some files may be missing in minimal setup

print("=== ALL DECISION POINTS ===")
q = """
PREFIX ex: <http://example.org/ontology/colorectal-triage#>
SELECT ?label ?importance
WHERE {
  ?d a ex:TriageDecisionPoint ;
     ex:decision ?label ;
     ex:importance ?importance .
}
"""
for row in g.query(q):
    print(dict(row))
