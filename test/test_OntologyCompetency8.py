import unittest
import utility.TestUtilities as tu
from owlready2 import *

'''
Competency ID: 08
User: Maintenance Engineer
Competency Question: Does my inspection procedure check all the failure modes outlined in the Failure Modes and Effects Analysis (FMEA) that was used in my RCM?
'''
class TestOntologyCompetency7(unittest.TestCase):

    query = """
        prefix spo: <http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#>
        prefix cmto: <http://spec.equonto.org/ontology/maintenance-procedure/conditional-maintenance-task-ontology#>
        prefix iso: <http://rds.posccaesar.org/ontology/lis14/rdl/>

        SELECT ?functional_failure
        WHERE {
            VALUES ?failure_modes_in_fmea { cmto:NOI } .
            VALUES ?maintainable_item { cmto:maintainable_item_001 } .
            VALUES ?procedure_process { cmto:procedure_process_001 }
            ?functional_failure cmto:addressedBy ?corrective_maint_task; a cmto:FunctionalFailure .
            ?corrective_maint_task iso:activityPartOf ?procedure_process .
            ?failure_mode iso:isAbout ?functional_failure 
            FILTER NOT EXISTS {
                ?functional_failure iso:representedIn ?failure_modes_in_fmea
            }
        }
    """

    def setUp(self):
        tu.prepare_ontologies()
        self.ontologies = tu.load_ontology()

    def tearDown(self):
        self.ontologies = None
        tu.clear_staging()

    #def test_failueModeFromFmeaIsFoundInProcedure_shouldReturnEmptyList(self):
        


    # TODO: come back to this


if __name__ == '__main__':
    unittest.main()

# <these tests are developed with the help of GitHub co-pilot>