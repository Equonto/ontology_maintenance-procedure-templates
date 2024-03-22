import unittest
import utility.TestUtilities as tu
from owlready2 import *

'''
This test class checks that key consistency checks in OMPD are working. If the ontology is inconsistent, reasoning errors should be thrown.
'''
class TestOntologyConsistencyChecking(unittest.TestCase):

    def setUp(self):
        tu.prepare_ontologies()
        self.ontologies = tu.load_ontology()

    def tearDown(self):
        self.ontologies = None
        tu.clear_staging()

    def test_singleTaskIsADirectActivityPartOfTwoDifferentProcedures_shouldThrowReasongingError(self):
        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            proc1 = namespace.MaintenanceProcedureProcess("procedure_process_001")
            proc2 = namespace.MaintenanceProcedureProcess("procedure_process_002")
            task1 = namespace.MaintenanceTask("task_001")
            task1.directActivityPartOf.append(proc1)
            task1.directActivityPartOf.append(proc2)
            AllDifferent([proc1, proc2]) 
            with self.assertRaises(OwlReadyInconsistentOntologyError):
                tu.run_pellet_reasoner()
        namespace.destroy()

    def test_singleTaskIsADirectActivityPartofTwoTasks_shouldThrowReasoningError(self):
        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            task_top1 = namespace.MaintenanceTask("task_top1")
            task_top2 = namespace.MaintenanceTask("task_top2")
            task1 = namespace.MaintenanceTask("task_001")
            task1.directActivityPartOf.append(task_top1)
            task1.directActivityPartOf.append(task_top2)
            AllDifferent([task_top1, task_top2])
            with self.assertRaises(OwlReadyInconsistentOntologyError):
                tu.run_pellet_reasoner()
        namespace.destroy()

    def test_twoTasksAreDirectlyAfterOneTask_shouldThrowReasoningError(self):
        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            task1 = namespace.MaintenanceTask("task_001")
            task2 = namespace.MaintenanceTask("task_002")
            task3 = namespace.MaintenanceTask("task_003")
            task2.directlyAfter.append(task1)
            task3.directlyAfter.append(task1)
            AllDifferent([task2, task3])
            with self.assertRaises(OwlReadyInconsistentOntologyError):
                tu.run_pellet_reasoner()
        namespace.destroy()


    def test_maintenanceTaskIsADirectAcitivtyPartOfItself_shouldThrowReasoningError(self):
        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            proc1 = namespace.MaintenanceProcedureProcess("procedure_process_001")
            proc1.directActivityPartOf.append(proc1)
            with self.assertRaises(OwlReadyInconsistentOntologyError):
                tu.run_pellet_reasoner()
        namespace.destroy()

    def test_maintenanceTaskIsDirectlyAfterItself_shouldThrowAReasoningError(self):
        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            task1 = namespace.MaintenanceTask("task_001")
            task1.directlyAfter.append(task1)
            with self.assertRaises(OwlReadyInconsistentOntologyError):
                tu.run_pellet_reasoner()
        namespace.destroy()

    def test_maintenanceTaskIsLocallyEquivalentToEntityThatIsNotAProcess_shouldThrowReasoningError(self):
        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            task1 = namespace.MaintenanceTask("task_001")
            obj1 = namespace.MaintenanceTaskDescription("object_001")
            task1.locallyEquivalentTo.append(obj1)
            with self.assertRaises(OwlReadyInconsistentOntologyError):
                tu.run_pellet_reasoner()
        namespace.destroy()


if __name__ == '__main__':
    unittest.main()

# <these tests are developed with the help of GitHub co-pilot>