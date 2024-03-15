import unittest
import utility.TestUtilities as tu
from owlready2 import *

'''
Competency ID: 03
User: Maintenance Technician
Competency Question: Given that I am up to task x in a procedure, what tasks needs to be performed next.
'''
class TestOntologyCompetency3(unittest.TestCase):

    query = """
    prefix spo: <http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#>
    prefix iso: <http://rds.posccaesar.org/ontology/lis14/rdl/>

    SELECT ?next_maintenance_task 
    WHERE {
        VALUES ?current_maintenance_task { spo:task_001 } 
        ?next_maintenance_task spo:directlyAfter ?current_maintenance_task .
    }
    """

    def setUp(self):
        tu.prepare_ontologies()
        self.ontologies = tu.load_ontology()

    def tearDown(self):
        self.ontologies = None
        tu.clear_staging()

    def test_nextMaintenanceTaskExistsAtTopLevel_shouldReturnNextMaintenanceTask(self):
        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            task1 = namespace.MaintenanceTask("task_001")
            task2 = namespace.MaintenanceTask("task_002")
            task2.directlyAfter.append(task1) # note quirk in owlready where you cannot query direct inverse but you can access it in code
            tu.run_pellet_reasoner()
            result = tu.run_query(self.query)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0][0], task2)
        namespace.destroy()

    def test_noNextMaintenanceTaskExists_shouldReturnEmptyList(self):
        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            task1 = namespace.MaintenanceTask("task_001")
            tu.run_pellet_reasoner()
            result = tu.run_query(self.query)
            self.assertEqual(len(result), 0)
        namespace.destroy()

    def test_mainenanceTaskExistsAtNestedLevel_shouldOnlyReturnItemsAtSameLevel(self):
        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            task1 = namespace.MaintenanceTask("task_001")
            task2 = namespace.MaintenanceTask("task_002")
            task2.directActivityPartOf.append(task1)
            tu.run_pellet_reasoner()
            result = tu.run_query(self.query)
            self.assertEqual(len(result), 0)

    def test_multipleSubsequentTasksExist_shouldOnlyReturnNextTask(self):
        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            task1 = namespace.MaintenanceTask("task_001")
            task2 = namespace.MaintenanceTask("task_002")
            task3 = namespace.MaintenanceTask("task_003")
            task2.directlyAfter.append(task1)
            task3.directlyAfter.append(task2)
            tu.run_pellet_reasoner()
            result = tu.run_query(self.query)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0][0], task2)
        namespace.destroy()
