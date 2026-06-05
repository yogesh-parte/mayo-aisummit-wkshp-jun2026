from rdflib import Graph, Namespace, Literal
from rdflib.plugins.sparql import prepareQuery
from typing import List, Dict
import json

# Namespaces
EX = Namespace("http://example.org/ontology/colorectal-triage#")
PROV = Namespace("http://www.w3.org/ns/prov#")
DCTERMS = Namespace("http://purl.org/dc/terms/")
NP = Namespace("http://www.nanopub.org/nschema#")
FHIR = Namespace("http://hl7.org/fhir/")

class ColorectalTriageAgent:
    def __init__(self):
        self.graph = Graph()
        self.loaded = False

    def load_nanopublications(self, trig_files: List[str]):
        """Load one or more TRIG nanopublication files"""
        for file_path in trig_files:
            try:
                self.graph.parse(file_path, format="trig")
                print(f"Loaded: {file_path}")
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
        self.loaded = True
        print(f"Total triples loaded: {len(self.graph)}")

    def get_triage_recommendation(self, patient_id: str) -> List[Dict]:
        """Local query: Get triage recommendation for a patient"""
        
        query = prepareQuery("""
        PREFIX fhir: <http://hl7.org/fhir/>
        PREFIX dcterms: <http://purl.org/dc/terms/>
        PREFIX prov: <http://www.w3.org/ns/prov#>
        PREFIX ex: <http://example.org/ontology/colorectal-triage#>
        PREFIX np: <http://www.nanopub.org/nschema#>

        SELECT 
          ?patientId 
          ?cancerType 
          ?isMetastatic 
          ?msiStatus 
          ?isEmergency 
          ?recommendedPathway
          ?importance
          ?sourceTitle
          ?decisionLabel
        WHERE {
          # Patient FHIR Data
          ?patient a fhir:Patient ;
                   fhir:id [ fhir:v ?patientId ] .

          ?condition a fhir:Condition ;
                     fhir:subject ?patient ;
                     fhir:code [ fhir:coding [ fhir:code [ fhir:v ?cancerCode ] ] ] .

          BIND( IF(CONTAINS(?cancerCode, "C20") || CONTAINS(?cancerCode, "rectum"), "Rectal", "Colon") AS ?cancerType )

          OPTIONAL { 
            ?condition fhir:stage [ fhir:summary [ fhir:text [ fhir:v ?stageText ] ] ] .
            BIND(CONTAINS(?stageText, "IV") || CONTAINS(?stageText, "metastatic") AS ?isMetastatic)
          }

          OPTIONAL {
            ?msiObs a fhir:Observation ;
                    fhir:subject ?patient ;
                    fhir:valueCodeableConcept [ fhir:coding [ fhir:code [ fhir:v ?msiStatus ] ] ] .
          }

          OPTIONAL {
            ?emerg a fhir:Condition ;
                   fhir:subject ?patient ;
                   fhir:code [ fhir:coding [ fhir:code [ fhir:v ?emergCode ] ] ] .
            BIND(CONTAINS(?emergCode, "obstruction") || CONTAINS(?emergCode, "emergency") AS ?isEmergency)
          }

          # Match with nanopublication assertions
          ?nanopub a np:Nanopublication ;
                   np:hasAssertion ?assertionGraph .

          GRAPH ?assertionGraph {
            ?decision a ex:TriageDecisionPoint ;
                      ex:decision ?decisionLabel ;
                      ex:importance ?importance .
          }

          OPTIONAL {
            ?source dcterms:title ?sourceTitle .
          }

          # Triage decision logic
          BIND(
            IF(?isEmergency = true, "URGENT: Surgical consultation (Obstructing/Emergency)",
              IF(?cancerType = "Rectal", "Multidisciplinary evaluation (MedOnc, RadOnc, SurgOnc)",
                IF(?isMetastatic = true, "Medical Oncology + Molecular Testing",
                  IF(?msiStatus IN ("MSI-H", "dMMR"), "Immunotherapy consideration",
                    "Surgical Oncology evaluation"))))
            AS ?recommendedPathway
          )
        }
        ORDER BY DESC(?importance)
        """, initNs={"fhir": FHIR, "ex": EX, "prov": PROV, "dcterms": DCTERMS, "np": NP})

        results = self.graph.query(query, initBindings={"patientId": Literal(patient_id)})
        
        output = []
        for row in results:
            output.append({str(k): str(v) for k, v in row.asdict().items()})
        return output

    def explain_recommendation(self, decision_label: str) -> List[Dict]:
        """Explain a specific decision point with provenance"""
        
        query = prepareQuery("""
        PREFIX dcterms: <http://purl.org/dc/terms/>
        PREFIX prov: <http://www.w3.org/ns/prov#>
        PREFIX ex: <http://example.org/ontology/colorectal-triage#>
        PREFIX np: <http://www.nanopub.org/nschema#>

        SELECT ?decisionLabel ?description ?importance ?sourceTitle ?createdDate
        WHERE {
          ?nanopub a np:Nanopublication ;
                   np:hasAssertion ?ag ;
                   dcterms:created ?createdDate .

          GRAPH ?ag {
            ?decision a ex:TriageDecisionPoint ;
                      ex:decision ?decisionLabel ;
                      ex:description ?description ;
                      ex:importance ?importance .
          }

          OPTIONAL {
            ?decision prov:wasDerivedFrom ?source .
            ?source dcterms:title ?sourceTitle .
          }

          FILTER(?decisionLabel = ?decisionLabelFilter)
        }
        """, initNs={"ex": EX, "prov": PROV, "dcterms": DCTERMS, "np": NP})

        results = self.graph.query(query, initBindings={"decisionLabelFilter": Literal(decision_label)})
        
        output = []
        for row in results:
            output.append({str(k): str(v) for k, v in row.asdict().items()})
        return output


# ========================== EXAMPLE USAGE ==========================

if __name__ == "__main__":
    agent = ColorectalTriageAgent()
    
    # Load nanopublications + patient FHIR data
    files = [
        "data/nanopubs/colorectal_framework.np.trig",
        "data/nanopubs/rectal_vs_colon.np.trig",
        "data/nanopubs/metastatic_vs_non.np.trig",
        "data/nanopubs/mmr_msi.np.trig",
        "data/nanopubs/obstructing_emergency.np.trig",
        "data/patient-example-12345.ttl"
    ]
    
    agent.load_nanopublications(files)

    print("\n=== Triage Recommendation for PATIENT-12345 ===")
    results = agent.get_triage_recommendation("PATIENT-12345")
    
    for r in results:
        print(json.dumps(r, indent=2))
        print("-" * 80)

    print("\n=== Explanation for Rectal vs. Colon ===")
    explanation = agent.explain_recommendation("Rectal vs. Colon")
    for exp in explanation:
        print(json.dumps(exp, indent=2))
