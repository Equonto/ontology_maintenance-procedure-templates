import unittest
import utility.TestUtilities as tu
from owlready2 import *

'''
Competency ID: 02
User: Maintenance Technician
Competency Question: What steps need to be performed to execute my procedure?
'''
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

    def test_singleMaintenanceTaskAtTopLevel_shouldReturnMaintenanceTask(self):
        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            proc1 = namespace.MaintenanceProcedureProcess("procedure_process_001")
            task1 = namespace.MaintenanceTask("task_001")
            task1.directActivityPartOf.append(proc1)
            tu.run_pellet_reasoner()
            result = tu.run_query(self.query)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0][0], task1)
        namespace.destroy()

    def test_multipleMaintenanceTasksAtTopLevel_shouldReturnAllMaintenanceTasks(self):
        
        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            proc1 = namespace.MaintenanceProcedureProcess("procedure_process_001")
            task1 = namespace.MaintenanceTask("task_001")
            task1.directActivityPartOf.append(proc1)
            task2 = namespace.MaintenanceTask("task_002")
            task2.directActivityPartOf.append(proc1)
            tu.run_pellet_reasoner()
            result = tu.run_query(self.query)
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0][0], task1)
            self.assertEqual(result[1][0], task2)
        namespace.destroy()

    def test_multipleMainteananceTasksAtDifferentNestingLevels_shouldReturnAllMaintenanceTasks(self):
    
        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            proc1 = namespace.MaintenanceProcedureProcess("procedure_process_001")
            task1 = namespace.MaintenanceTask("task_001")
            task1.directActivityPartOf.append(proc1)
            task2 = namespace.MaintenanceTask("task_002")
            task2.directActivityPartOf.append(task1)
            task3 = namespace.MaintenanceTask("task_003")
            task3.directActivityPartOf.append(task2)
            tu.run_pellet_reasoner()
            result = tu.run_query(self.query)
            self.assertEqual(len(result), 3)
            self.assertEqual(result[0][0], task1)
            self.assertEqual(result[0][1], proc1)
            self.assertEqual(result[1][0], task2)
            self.assertEqual(result[1][1], task1)
            self.assertEqual(result[2][0], task3)
            self.assertEqual(result[2][1], task2)

        namespace.destroy()

    def test_maintenanceTaskInDifferentProcedure_shouldNotReturnMaintenanceTask(self):
        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            proc1 = namespace.MaintenanceProcedureProcess("procedure_process_001")
            proc2 = namespace.MaintenanceProcedureProcess("procedure_process_002")
            task1 = namespace.MaintenanceTask("task_001")
            task1.directActivityPartOf.append(proc2)
            tu.run_pellet_reasoner()
            result = tu.run_query(self.query)
            self.assertEqual(len(result), 0)
        namespace.destroy()

if __name__ == '__main__':
    unittest.main()

# <these tests are developed with the help of GitHub co-pilot>