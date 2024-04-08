import unittest
import utility.TestUtilities as tu
from owlready2 import *

'''
Competency ID: 06
User: Maintenance Engineer
Competency Question: There has been a change in the regulations and an existing permit needs to be modified. Which procedures use this permit?
'''
class TestOntologyCompetency6(unittest.TestCase):

    query = """
        prefix spo: <http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#>
        prefix iso: <http://rds.posccaesar.org/ontology/lis14/rdl/>

        SELECT ?maintenance_process
        where {
            VALUES ?permit { spo:permit_001 } 
            ?permit iso:participantIn ?maintenance_process .
            ?permit a spo:Permit .
            ?maintenance_process a spo:MaintenanceProcess .
        }
    """

    def setUp(self):
        tu.prepare_ontologies()
        self.ontologies = tu.load_ontology()

    def tearDown(self):
        self.ontologies = None
        tu.clear_staging()

    def test_permitExists_shoulReturnProcedure(self):
        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            permit1 = namespace.Permit("permit_001")
            proc1 = namespace.MaintenanceProcess("maintenance_process_001")
            permit1.requirementOf.append(proc1)
            tu.run_pellet_reasoner()
            result = tu.run_query(self.query)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0][0], proc1)

        namespace.destroy()

    def test_permitRequiredForMultipleProcedures_shouldReturnAllProcedures(self):
        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            permit1 = namespace.Permit("permit_001")
            proc1 = namespace.MaintenanceProcess("maintenance_process_001")
            proc2 = namespace.MaintenanceProcess("maintenance_process_002")
            permit1.requirementOf.append(proc1)
            permit1.requirementOf.append(proc2)
            tu.run_pellet_reasoner()
            result = tu.run_query(self.query)
            self.assertEqual(len(result), 2)
            self.assertEqual(result[1][0], proc1) # TODO: check if these are consistently returning the right way arround
            self.assertEqual(result[0][0], proc2)
    
        namespace.destroy()

    def test_permitNotRequiredForAnyProcedure_shouldReturnEmptyList(self):
        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            permit1 = namespace.Permit("permit_001")
            tu.run_pellet_reasoner()
            result = tu.run_query(self.query)
            self.assertEqual(len(result), 0)

        namespace.destroy()

    def test_permitRequiredAtTaskLevel_shouldReturnProcedureButNotTask(self):
        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            permit1 = namespace.Permit("permit_001")
            proc1 = namespace.MaintenanceProcess("maintenance_process_001")
            task1 = namespace.MaintenanceTask("maintenance_task_001")
            task1.directActivityPartOf.append(proc1)
            permit1.requirementOf.append(task1)
            tu.run_pellet_reasoner()
            result = tu.run_query(self.query)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0][0], proc1)

        namespace.destroy()

    def test_permitRequiredAtNestedTaskLevel_shouldReturnProcedureButNotTask(self):
        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            permit1 = namespace.Permit("permit_001")
            proc1 = namespace.MaintenanceProcess("maintenance_process_001")
            task1 = namespace.MaintenanceTask("maintenance_task_001")
            task2 = namespace.MaintenanceTask("maintenance_task_002")
            task2.directActivityPartOf.append(task1)
            task1.directActivityPartOf.append(proc1)
            permit1.requirementOf.append(task2)
            tu.run_pellet_reasoner()
            result = tu.run_query(self.query)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0][0], proc1)

        namespace.destroy()

    def test_differentPermitRequiredForProcedure_shouldReturnEmptyList(self):
        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            permit1 = namespace.Permit("permit_001")
            permit2 = namespace.Permit("permit_002")
            proc1 = namespace.MaintenanceProcess("maintenance_process_001")
            permit2.requirementOf.append(proc1)
            tu.run_pellet_reasoner()
            result = tu.run_query(self.query)
            self.assertEqual(len(result), 0)
            
        namespace.destroy()





if __name__ == '__main__':
    unittest.main()

# <these tests are developed with the help of GitHub co-pilot>