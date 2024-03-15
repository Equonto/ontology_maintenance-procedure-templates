
from owlready2 import *
import rdflib
import os
import imp

# read ttl file and save OWL file in staging
def prepare_ontologies():
    ontology_filenames = os.listdir("ontology")
    for ontology_filename in ontology_filenames:
        g = rdflib.Graph()
        format = ontology_filename.split(".")[1]
        if format == "owl" or format == "rdf":
            format = "xml"
        if ((format == "ttl" or format == "xml") and ontology_filename != "catalog-v001.xml"):
            g.parse("ontology/"+ontology_filename, format=format)
            ontology_filename = ontology_filename.replace(format, "xml")
            g.serialize(destination="test/staging/"+ontology_filename, format="xml")


# Loads a .ttl file with no instances from the ontology folder (with imported ontologies)
def load_ontology():
    path = "test/staging/"
    iso = owlready2.get_ontology("file://"+path+"iso.owl")
    iso.load()
    annotation_vocabulary = owlready2.get_ontology("file://"+path+"AnnotationVocabulary.rdf")
    annotation_vocabulary.load()
    spo = owlready2.get_ontology("file://"+path+"StaticProcedureOntology_v0_0_1.xml")
    spo.load()
    ontology = owlready2.get_ontology("file://"+path+"ConditionalMaintenanceTaskOntology_v0_0_1.xml")

    # add imported ontologies
    spo.imported_ontologies.append(iso)
    spo.imported_ontologies.append(annotation_vocabulary)
    ontology.imported_ontologies.append(spo)

    ontology.load()

    ontologies = {
        "iso": iso,
        "annotation_vocabulary": annotation_vocabulary,
        "spo": spo,
        "cmto": ontology
    }
    return ontologies

# run#s a Hermit reasoner on the ontology with owlready 2
def run_hermit_reasoner():
    sync_reasoner(infer_property_values = True)

def run_pellet_reasoner():
    sync_reasoner_pellet(infer_property_values = True, infer_data_property_values=True)

def run_query(query):
    results = default_world.sparql(query)
    return list(results)

# clear test/ staging file
def clear_staging():
    for filename in os.listdir("test/staging"):
        os.remove("test/staging/"+filename)


