import unittest
import utility.TestUtilities as tu
from owlready2 import *

class TestOntologyCompetency2(unittest.TestCase):

    query = """
    prefix spo: <http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#>
    prefix iso: <http://rds.posccaesar.org/ontology/lis14/rdl/>

    SELECT ?maintenance_task ?parent
    WHERE {
        VALUES ?procedure_process { spo:procedure_process_001 } 
        ?maintenance_task iso:activityPartOf ?procedure_process .
        ?maintenance_task spo:directActivityPartOf ?parent .
    }
    """

    def setUp(self):
        tu.prepare_ontologies()
        self.ontologies = tu.load_ontology()

    def tearDown(self):
        self.ontologies = None
        tu.clear_staging()

    def test_single_maintenance_task(self):
        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
                
        # arrage
        with namespace:
            proc1 = namespace.MaintenanceProcedureProcess("procedure_process_001")
            task1 = namespace.MaintenanceTask("task_001")
            task1.directActivityPartOf.append(proc1)

            tu.run_pellet_reasoner()
            # act
            result = tu.run_query(self.query)
            
            # assert that list has one entry
            self.assertEqual(len(result), 1)

            # assert that the resource found is the tool_001
            self.assertEqual(result[0][0], task1)


if __name__ == '__main__':
    unittest.main()
