import unittest
import utility.TestUtilities as tu
from owlready2 import *

'''
Competency ID: 05
User: Maintenance Technician
Competency Question: What corrective action does my procedure suggest on observation of a failure mode in my inspection?
'''
class TestOntologyCompetency5(unittest.TestCase):

    query = """
    prefix spo: <http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#>
    prefix cmto: <http://spec.equonto.org/ontology/maintenance-procedure/conditional-maintenance-task-ontology#>
    prefix iso: <http://rds.posccaesar.org/ontology/lis14/rdl/>

    SELECT ?corrective_maintenance_task
    WHERE {
        cmto:functional_failure_001 cmto:addressedBy ?corrective_maintenance_task .
        ?corrective_maintenance_task iso:activityPartOf cmto:procedure_process_001; a cmto:CorrectiveMaintenanceTask .
    }
    """

    def setUp(self):
        tu.prepare_ontologies()
        self.ontologies = tu.load_ontology()

    def tearDown(self):
        self.ontologies = None
        tu.clear_staging()

    def test_singleCorrectiveMaintenanceTaskExists_shouldReturnCorrectiveMaintenanceTask(self):
        spo = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        cmto = self.ontologies["cmto"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/conditional-maintenance-task-ontology#")

        with spo, cmto:
            proc1 = spo.MaintenanceProcedureProcess("procedure_process_001")
            ff = cmto.FunctionalFailure("functional_failure_001")
            maintenance_task = spo.MaintenanceTask("corrective_maintenance_task_001")
            ff.addressedBy.append(maintenance_task)
            maintenance_task.directActivityPartOf.append(proc1)
            tu.run_pellet_reasoner()

            result = tu.run_query(self.query) 

            self.assertEqual(len(result), 1)
            self.assertEqual(result[0][0], maintenance_task)
        
        spo.destroy()
        cmto.destroy()

    def test_multipleCorrectiveMaintenanceTasksExist_shouldReturnOnlyTheCorrectOne(self):
        spo = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        cmto = self.ontologies["cmto"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/conditional-maintenance-task-ontology#")

        with spo, cmto:
            proc1 = spo.MaintenanceProcedureProcess("procedure_process_001")
            ff = cmto.FunctionalFailure("functional_failure_001")
            ff2 = cmto.FunctionalFailure("functional_failure_002")
            maintenance_task1 = spo.MaintenanceTask("corrective_maintenance_task_001")
            maintenance_task2 = spo.MaintenanceTask("corrective_maintenance_task_002")
            ff.addressedBy.append(maintenance_task1)
            ff2.addressedBy.append(maintenance_task2)
            maintenance_task1.directActivityPartOf.append(proc1)
            maintenance_task2.directActivityPartOf.append(proc1)
            tu.run_pellet_reasoner()

            result = tu.run_query(self.query)

            self.assertEqual(len(result), 1)
            self.assertEqual(result[0][0], maintenance_task1)
        
        spo.destroy()
        cmto.destroy()

    def test_noCorrectiveMaintenanceTaskAddressesFunctionalFailure_shouldReturnEmptyList(self):
        spo = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        cmto = self.ontologies["cmto"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/conditional-maintenance-task-ontology#")

        with spo, cmto:
            proc1 = spo.MaintenanceProcedureProcess("procedure_process_001")
            ff = cmto.FunctionalFailure("functional_failure_001")
            maintenance_task = spo.MaintenanceTask("corrective_maintenance_task_001")
            maintenance_task.directActivityPartOf.append(proc1)
            tu.run_pellet_reasoner()
            result = tu.run_query(self.query)
            self.assertEqual(len(result), 0)
        
        spo.destroy()
        cmto.destroy()

    def test_correctiveMaintenanceTaskAppearsInDifferentProcedure_shouldReturnEmptyList(self):
        spo = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        cmto = self.ontologies["cmto"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/conditional-maintenance-task-ontology#")

        with spo, cmto:
            proc1 = spo.MaintenanceProcedureProcess("procedure_process_001")
            proc2 = spo.MaintenanceProcedureProcess("procedure_process_002")
            ff = cmto.FunctionalFailure("functional_failure_001")
            maintenance_task = spo.MaintenanceTask("corrective_maintenance_task_001")
            ff.addressedBy.append(maintenance_task)
            maintenance_task.directActivityPartOf.append(proc2)
            tu.run_pellet_reasoner()
            result = tu.run_query(self.query)
            self.assertEqual(len(result), 0)
        
        spo.destroy()
        cmto.destroy()


if __name__ == '__main__':
    unittest.main()

# <these tests are developed with the help of GitHub co-pilot>