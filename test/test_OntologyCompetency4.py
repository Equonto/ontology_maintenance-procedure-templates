import unittest
import utility.TestUtilities as tu
from owlready2 import *

'''
Competency ID: 04
User: Maintenance Technician
Competency Question: Does my assigned procedure have any safety hazards that I need to be aware of?
'''
class TestOntologyCompetency4(unittest.TestCase):

    query = """
    prefix spo: <http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#>
    prefix iso: <http://rds.posccaesar.org/ontology/lis14/rdl/>

    SELECT ?hazard
    WHERE {
        VALUES ?procedure_process { spo:procedure_process_001 }
        ?hazard_realization_process iso:occursRelativeTo ?procedure_process .
        ?hazard_realization_process iso:realizes ?hazard .
        ?hazard a spo:Hazard 
    }
    """




if __name__ == '__main__':
    unittest.main()