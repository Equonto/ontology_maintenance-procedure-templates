import unittest
import utility.TestUtilities as tu
from owlready2 import *

'''
Competency ID: 08
User: Maintenance Planner
Competency Question: What resources to I require to execute this week's procedures?
'''
class TestOntologyCompetency7(unittest.TestCase):

    query = """
        prefix spo: <http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#>
        prefix cmto: <http://spec.equonto.org/ontology/maintenance-procedure/conditional-maintenance-task-ontology#>
        prefix iso: <http://rds.posccaesar.org/ontology/lis14/rdl/>

        SELECT ?resource {
        VALUES ?procedure_process { spo:procedure_process_001 spo:procedure_process_002 } 
        ?resource iso:participantIn ?procedure_process; a spo:Resource
    }
            
    """

    def setUp(self):
        tu.prepare_ontologies()
        self.ontologies = tu.load_ontology()

    def tearDown(self):
        self.ontologies = None
        tu.clear_staging()

    def test_singleResourceExistsInOneProcedure_shouldReturnResource(self):
        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            proc1 = namespace.MaintenanceProcedureProcess("procedure_process_001")
            proc2 = namespace.MaintenanceProcedureProcess("procedure_process_002")
            resource1 = namespace.Tool("tool_001")
            resource1.participantIn.append(proc1)
            resourceRole = namespace.ResourceRole("role_001")
            resource1.hasRole.append(resourceRole)
            tu.run_pellet_reasoner()
            result = tu.run_query(self.query)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0][0], resource1)

        namespace.destroy()

    def test_singleResourceExistsInBothProcedures_shouldReturnBothResources(self):
        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            proc1 = namespace.MaintenanceProcedureProcess("procedure_process_001")
            proc2 = namespace.MaintenanceProcedureProcess("procedure_process_002")
            resource1 = namespace.Tool("tool_001")
            resource2 = namespace.Tool("tool_002")
            resource1.participantIn.append(proc1)
            resource2.participantIn.append(proc2)
            resourceRole = namespace.ResourceRole("role_001")
            resource1.hasRole.append(resourceRole)
            resource2.hasRole.append(resourceRole)
            tu.run_pellet_reasoner()
            result = tu.run_query(self.query)
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0][0], resource1)
            self.assertEqual(result[1][0], resource2)

        namespace.destroy()

    def test_noResourcesExist_shouldReturnEmptyList(self):
        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            proc1 = namespace.MaintenanceProcedureProcess("procedure_process_001")
            proc2 = namespace.MaintenanceProcedureProcess("procedure_process_002")
            tu.run_pellet_reasoner()
            result = tu.run_query(self.query)
            self.assertEqual(len(result), 0)

        namespace.destroy()

    def test_resourceRequiredAtTaskLevel_shouldReturnResource(self):
        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            proc1 = namespace.MaintenanceProcedureProcess("procedure_process_001")
            proc2 = namespace.MaintenanceProcedureProcess("procedure_process_002")
            task1 = namespace.MaintenanceTask("task_001")
            task1.directActivityPartOf.append(proc1)
            resource1 = namespace.Tool("tool_001")
            resource1.participantIn.append(task1)
            resourceRole = namespace.ResourceRole("role_001")
            resource1.hasRole.append(resourceRole)
            tu.run_pellet_reasoner()
            result = tu.run_query(self.query)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0][0], resource1)

        namespace.destroy()


if __name__ == '__main__':
    unittest.main()

# <these tests are developed with the help of GitHub co-pilot>