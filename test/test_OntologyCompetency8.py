import unittest
import utility.TestUtilities as tu
from owlready2 import *

'''
Competency ID: 08
User: Maintenance Engineer
Competency Question: Does my Failure Mode and Effects Analysis (FMEA) that was used in my RCM contain all the functional failures that are checked in my procedure?
'''
class TestOntologyCompetency8(unittest.TestCase):

    query = """
        prefix spo: <http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#>
        prefix cmto: <http://spec.equonto.org/ontology/maintenance-procedure/conditional-maintenance-task-ontology#>
        prefix iso: <http://rds.posccaesar.org/ontology/lis14/rdl/>

        SELECT ?functional_failure
        WHERE {
            VALUES ?failure_modes_in_fmea { cmto:NOI } .
            VALUES ?maintainable_item { cmto:maintainable_item_001 } .
            VALUES ?procedure_process { cmto:procedure_process_001 } .
            ?functional_failure cmto:addressedBy ?corrective_maint_task; a cmto:FunctionalFailure .
            ?corrective_maint_task iso:activityPartOf ?procedure_process .
            ?maintainable_item iso:participantIn ?procedure_process .
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

    def test_procedureChecksFailureModesFromFmea_shouldReturnNoRemainingFailures(self):
        spo = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        cmto = self.ontologies["cmto"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/conditional-maintenance-task-ontology#")
        with spo, cmto:
            maintainable_item = spo.MaintainableItem("maintainable_item_001")
            procedure_process = spo.MaintenanceProcedureProcess("procedure_process_001")
            maintainable_item.participantIn.append(procedure_process)
            functional_failure = cmto.FunctionalFailure("functional_failure_001")
            corrective_maint_task = cmto.CorrectiveMaintenanceTask("corrective_maint_task_001")
            functional_failure.addressedBy.append(corrective_maint_task)
            corrective_maint_task.directActivityPartOf.append(procedure_process)
            failure_mode = cmto.FailureModeObservation("NOI")
            functional_failure.representedIn.append(failure_mode)
            tu.run_pellet_reasoner()
            result = tu.run_query(self.query)
            self.assertEqual(len(result), 0)
        spo.destroy()
        cmto.destroy()

    def test_procedureChecksFailureModesThatAreNotInFmea_shouldReturnReturnRemainingFailureModes(self):
        spo = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        cmto = self.ontologies["cmto"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/conditional-maintenance-task-ontology#")
        with spo, cmto:
            maintainable_item = spo.MaintainableItem("maintainable_item_001")
            procedure_process = spo.MaintenanceProcedureProcess("procedure_process_001")
            maintainable_item.participantIn.append(procedure_process)
            functional_failure = cmto.FunctionalFailure("functional_failure_001")
            functional_failure_2 = cmto.FunctionalFailure("functional_failure_002")
            corrective_maint_task = cmto.CorrectiveMaintenanceTask("corrective_maint_task_001")
            functional_failure.addressedBy.append(corrective_maint_task)
            functional_failure_2.addressedBy.append(corrective_maint_task)
            corrective_maint_task.directActivityPartOf.append(procedure_process)
            failure_mode = cmto.FailureModeObservation("NOI")
            functional_failure.representedIn.append(failure_mode)
            failure_mode_2 = cmto.FailureModeObservation("NOI2")
            functional_failure_2.representedIn.append(failure_mode_2)
            tu.run_pellet_reasoner()
            result = tu.run_query(self.query)
            self.assertEqual(len(result), 1)
        spo.destroy()
        cmto.destroy()  

    def test_procedureChecksAlternativeFailures_shouldReturnRemainingFailures(self):
        spo = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        cmto = self.ontologies["cmto"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/conditional-maintenance-task-ontology#")
        with spo, cmto:
            maintainable_item = spo.MaintainableItem("maintainable_item_001")
            procedure_process = spo.MaintenanceProcedureProcess("procedure_process_001")
            maintainable_item.participantIn.append(procedure_process)
            functional_failure = cmto.FunctionalFailure("functional_failure_001")
            corrective_maint_task = cmto.CorrectiveMaintenanceTask("corrective_maint_task_001")
            functional_failure.addressedBy.append(corrective_maint_task)
            corrective_maint_task.directActivityPartOf.append(procedure_process)
            failure_mode = cmto.FailureModeObservation("alternative")
            functional_failure.representedIn.append(failure_mode)
            tu.run_pellet_reasoner()
            result = tu.run_query(self.query)
            self.assertEqual(len(result), 1)
        spo.destroy()
        cmto.destroy()

    def test_procedureChecksNoFailues_shouldReturnRemainingFailures(self):
        spo = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        cmto = self.ontologies["cmto"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/conditional-maintenance-task-ontology#")
        with spo, cmto:
            maintainable_item = spo.MaintainableItem("maintainable_item_001")
            procedure_process = spo.MaintenanceProcedureProcess("procedure_process_001")
            maintainable_item.participantIn.append(procedure_process)
            functional_failure = cmto.FunctionalFailure("functional_failure_001")
            corrective_maint_task = cmto.CorrectiveMaintenanceTask("corrective_maint_task_001")
            functional_failure.addressedBy.append(corrective_maint_task)
            corrective_maint_task.directActivityPartOf.append(procedure_process)
            tu.run_pellet_reasoner()
            result = tu.run_query(self.query)
            self.assertEqual(len(result), 1)
        spo.destroy()
        cmto.destroy()

if __name__ == '__main__':
    unittest.main()

# <these tests are developed with the help of GitHub co-pilot>