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

    def setUp(self):
        tu.prepare_ontologies()
        self.ontologies = tu.load_ontology()

    def tearDown(self):
        self.ontologies = None
        tu.clear_staging()

    def test_singleHazardSpecifiedAtProcedureLevel_shouldReturnHazard(self):
        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            proc1 = namespace.MaintenanceProcedureProcess("procedure_process_001")
            hazard1 = namespace.Hazard("hazard_001")
            hazard_realization_process = namespace.HazardRealizationProcess("hazard_realization_process_001")
            hazard_realization_process.occursRelativeTo.append(proc1)
            hazard_realization_process.realizes.append(hazard1)

            tu.run_pellet_reasoner()

            result = tu.run_query(self.query)

            self.assertEqual(len(result), 1)
            self.assertEqual(result[0][0], hazard1)
            
        namespace.destroy()

    def test_multipleHazardsSpecifiedAtProcedureLevel_shouldReturnHazards(self):
        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            proc1 = namespace.MaintenanceProcedureProcess("procedure_process_001")
            hazard1 = namespace.Hazard("hazard_001")
            hazard2 = namespace.Hazard("hazard_002")
            hazard_realization_process = namespace.HazardRealizationProcess("hazard_realization_process_001")
            hazard_realization_process.occursRelativeTo.append(proc1)
            hazard_realization_process.realizes.append(hazard1)
            hazard_realization_process_2 = namespace.HazardRealizationProcess("hazard_realization_process_002")
            hazard_realization_process_2.occursRelativeTo.append(proc1)
            hazard_realization_process_2.realizes.append(hazard2)

            tu.run_pellet_reasoner()

            result = tu.run_query(self.query)

            self.assertEqual(len(result), 2)
            self.assertTrue(hazard1 in [x[0] for x in result])
            self.assertTrue(hazard2 in [x[0] for x in result])

        namespace.destroy()

    def test_singleHazardAtTaskTopLevel_shouldReturnHazard(self):
            namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
            with namespace:
                proc1 = namespace.MaintenanceProcedureProcess("procedure_process_001")
                task1 = namespace.MaintenanceTask("task_001")
                task1.directActivityPartOf.append(proc1)
                hazard1 = namespace.Hazard("hazard_001")
                hazard_realization_process = namespace.HazardRealizationProcess("hazard_realization_process_001")
                hazard_realization_process.occursRelativeTo.append(task1)
                hazard_realization_process.realizes.append(hazard1)

                tu.run_pellet_reasoner()

                result = tu.run_query(self.query)

                self.assertEqual(len(result), 1)
                self.assertEqual(result[0][0], hazard1)
            
            namespace.destroy()
        
    def test_multipleHazardAtTaskTopLevel_shouldReturnHazards(self):
            namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
            with namespace:
                proc1 = namespace.MaintenanceProcedureProcess("procedure_process_001")
                task1 = namespace.MaintenanceTask("task_001")
                task1.directActivityPartOf.append(proc1)
                hazard1 = namespace.Hazard("hazard_001")
                hazard2 = namespace.Hazard("hazard_002")
                hazard_realization_process = namespace.HazardRealizationProcess("hazard_realization_process_001")
                hazard_realization_process.occursRelativeTo.append(task1)
                hazard_realization_process.realizes.append(hazard1)
                hazard_realization_process_2 = namespace.HazardRealizationProcess("hazard_realization_process_002")
                hazard_realization_process_2.occursRelativeTo.append(task1)
                hazard_realization_process_2.realizes.append(hazard2)

                tu.run_pellet_reasoner()

                result = tu.run_query(self.query)

                self.assertEqual(len(result), 2)
                self.assertTrue(hazard1 in [x[0] for x in result])
                self.assertTrue(hazard2 in [x[0] for x in result])

            namespace.destroy()
        
    def test_singleHazardAtTaskSecondLevel_shouldReturnHazard(self):
            namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
            with namespace:
                proc1 = namespace.MaintenanceProcedureProcess("procedure_process_001")
                task1 = namespace.MaintenanceTask("task_001")
                task1.directActivityPartOf.append(proc1)
                task2 = namespace.MaintenanceTask("task_002")
                task2.directActivityPartOf.append(task1)
                hazard1 = namespace.Hazard("hazard_001")
                hazard_realization_process = namespace.HazardRealizationProcess("hazard_realization_process_001")
                hazard_realization_process.occursRelativeTo.append(task2)
                hazard_realization_process.realizes.append(hazard1)

                tu.run_pellet_reasoner()

                result = tu.run_query(self.query)

                self.assertEqual(len(result), 1)
                self.assertEqual(result[0][0], hazard1)

            namespace.destroy()

    def test_multipleHazardAtTaskSecondLevel_shouldReturnHazard(self):
            namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
            with namespace:
                proc1 = namespace.MaintenanceProcedureProcess("procedure_process_001")
                task1 = namespace.MaintenanceTask("task_001")
                task1.directActivityPartOf.append(proc1)
                task2 = namespace.MaintenanceTask("task_002")
                task2.directActivityPartOf.append(task1)
                hazard1 = namespace.Hazard("hazard_001")
                hazard2 = namespace.Hazard("hazard_002")
                hazard_realization_process = namespace.HazardRealizationProcess("hazard_realization_process_001")
                hazard_realization_process.occursRelativeTo.append(task2)
                hazard_realization_process.realizes.append(hazard1)
                hazard_realization_process_2 = namespace.HazardRealizationProcess("hazard_realization_process_002")
                hazard_realization_process_2.occursRelativeTo.append(task2)
                hazard_realization_process_2.realizes.append(hazard2)

                tu.run_pellet_reasoner()

                result = tu.run_query(self.query)

                self.assertEqual(len(result), 2)
                self.assertTrue(hazard1 in [x[0] for x in result])
                self.assertTrue(hazard2 in [x[0] for x in result])

            namespace.destroy()

    def test_hazardBelongsToDifferentProcedureAtProcedureLevel_shouldNotReturnHazard(self):
            namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
            with namespace:
                proc1 = namespace.MaintenanceProcedureProcess("procedure_process_001")
                proc2 = namespace.MaintenanceProcedureProcess("procedure_process_002")
                hazard1 = namespace.Hazard("hazard_001")
                hazard_realization_process = namespace.HazardRealizationProcess("hazard_realization_process_001")
                hazard_realization_process.occursRelativeTo.append(proc2)
                hazard_realization_process.realizes.append(hazard1)
    
                tu.run_pellet_reasoner()
    
                result = tu.run_query(self.query)
    
                self.assertEqual(len(result), 0)

            namespace.destroy()
    
    def test_hazardBelongsToDifferentProcedureAtTaskLevel_shouldNotReturnHazard(self):
            namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
            with namespace:
                proc1 = namespace.MaintenanceProcedureProcess("procedure_process_001")
                proc2 = namespace.MaintenanceProcedureProcess("procedure_process_002")
                task1 = namespace.MaintenanceTask("task_001")
                task1.directActivityPartOf.append(proc2)
                hazard1 = namespace.Hazard("hazard_001")
                hazard_realization_process = namespace.HazardRealizationProcess("hazard_realization_process_001")
                hazard_realization_process.occursRelativeTo.append(task1)
                hazard_realization_process.realizes.append(hazard1)
    
                tu.run_pellet_reasoner()
    
                result = tu.run_query(self.query)
    
                self.assertEqual(len(result), 0)
                
            namespace.destroy()



if __name__ == '__main__':
    unittest.main()

# <these tests are developed with the help of GitHub co-pilot>