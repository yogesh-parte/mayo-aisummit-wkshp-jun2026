from rdflib import Graph
import json

g = Graph()
g.parse("colorectal_triage_single.np.trig", format="trig")

# Simple view query
q_simple = """
PREFIX ex: <http://example.org/ontology/colorectal-triage#>
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT ?decision ?label ?desc ?importance
WHERE {
  ?decision a ex:TriageDecisionPoint ;
            ex:decision ?label ;
            ex:description ?desc ;
            ex:importance ?importance .
}
"""

print("=== SIMPLE VIEW ===")
for row in g.query(q_simple):
    print(dict(row))

# Enriched view with provenance
q_enriched = """
PREFIX ex: <http://example.org/ontology/colorectal-triage#>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT ?decisionLabel ?desc ?importance ?sourceTitle
WHERE {
  ?decision a ex:TriageDecisionPoint ;
            ex:decision ?decisionLabel ;
            ex:description ?desc ;
            ex:importance ?importance .
  ?decision prov:wasDerivedFrom ?source .
  ?source dcterms:title ?sourceTitle .
}
"""

print("\n=== ENRICHED VIEW WITH PROVENANCE ===")
for row in g.query(q_enriched):
    print(dict(row))
