import unittest
import utility.TestUtilities as tu
import owlready2

'''
Competency ID: 01
User: Maintenance Technician
Competency Question: What tools, materials and permits do I require to execute a procedure?
'''
class TestOntologyCompetency1(unittest.TestCase):

    query = """
    prefix spo: <http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#>
    prefix iso: <http://rds.posccaesar.org/ontology/lis14/rdl/>

    SELECT ?resource
    WHERE {
        VALUES ?procedure_process { spo:procedure_process_001 } 
        VALUES ?type { spo:Tool spo:Material spo:Permit } 
        ?resource iso:participantIn ?procedure_process; a ?type 
    } 
    """

    def setUp(self):
        tu.prepare_ontologies()
        self.ontologies = tu.load_ontology()

    def tearDown(self):
        self.ontologies = None
        tu.clear_staging()

    def test_singleResource_shouldReturnSingleResource(self):

        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            proc1 = namespace.MaintenanceProcedureProcess("procedure_process_001")
            tool1 = namespace.Tool("tool_001")
            tool1.participantIn.append(proc1)
            tu.run_hermit_reasoner()
            result = tu.run_query(self.query)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0][0], tool1)

        namespace.destroy()

    def test_multipleResourcesOfSameType_shouldReturnMultipleResourcesOfSameType(self):

        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
                
        # arrage
        with namespace:
            proc1 = namespace.MaintenanceProcedureProcess("procedure_process_001")
            tool1 = namespace.Tool("tool_001")
            tool2 = namespace.Tool("tool_002")
            tool1.participantIn.append(proc1)
            tool2.participantIn.append(proc1)
            tu.run_hermit_reasoner()
            result = tu.run_query(self.query)
            self.assertEqual(len(result), 2)
            self.assertTrue(tool1 in [x[0] for x in result])
            self.assertTrue(tool2 in [x[0] for x in result])

        namespace.destroy()

    def test_mulipleResourcesOfDifferentType_shouldReturnMultipleResourcesOfDifferentType(self):

        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            proc1 = namespace.MaintenanceProcedureProcess("procedure_process_001")
            tool1 = namespace.Tool("tool_001")
            material1 = namespace.Material("material_001")
            permit1 = namespace.Permit("permit_001")
            tool1.participantIn.append(proc1)
            material1.participantIn.append(proc1)
            permit1.participantIn.append(proc1)
            tu.run_hermit_reasoner()
            result = tu.run_query(self.query)
            self.assertEqual(len(result), 3)
            self.assertTrue(tool1 in [x[0] for x in result])
            self.assertTrue(material1 in [x[0] for x in result])
            self.assertTrue(permit1 in [x[0] for x in result])
        namespace.destroy()


    def test_singleResourceInSingleLevelNestedTask_shouldReturnResourceFromNestedTask(self):

        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            proc1 = namespace.MaintenanceProcedureProcess("procedure_process_001")
            maintenance_task_1 = namespace.MaintenanceTask("maintenance_task_001")
            maintenance_task_1.directActivityPartOf.append(proc1)
            tool1 = namespace.Tool("tool_001")
            tool1.participantIn.append(maintenance_task_1)
            tu.run_hermit_reasoner()
            result = tu.run_query(self.query)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0][0], tool1)

        namespace.destroy()
            
    def test_singleResourceInMultiLevelNestedTask_shouldReturnResourceFromNestedTask(self):

        namespace = self.ontologies["spo"]
        with namespace:
            proc1 = namespace.MaintenanceProcedureProcess("procedure_process_001")
            maintenance_task_1 = namespace.MaintenanceTask("maintenance_task_001")
            maintenance_task_2 = namespace.MaintenanceTask("maintenance_task_002")
            maintenance_task_1.directActivityPartOf.append(proc1)
            maintenance_task_2.directActivityPartOf.append(maintenance_task_1)
            tool1 = namespace.Tool("tool_001")
            tool1.participantIn.append(maintenance_task_1)
            tool2 = namespace.Tool("tool_002")
            tool2.participantIn.append(maintenance_task_2)
            tu.run_hermit_reasoner()
            result = tu.run_query(self.query)
            self.assertEqual(len(result), 2)
            self.assertTrue(tool1 in [x[0] for x in result])
            self.assertTrue(tool2 in [x[0] for x in result])

        namespace.destroy()

    def test_singleResourceNotInDefinedTypes_shouldNotReturnResource(self):

        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            proc1 = namespace.MaintenanceProcedureProcess("procedure_process_001")
            resource1 = namespace.Resource("resource_001")
            resource1.participantIn.append(proc1)
            tu.run_hermit_reasoner()
            result = tu.run_query(self.query)
            self.assertEqual(len(result), 0)
        namespace.destroy()

    def test_singleResourceInDifferentProcedure_shouldNotReturnResource(self):

        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            proc1 = namespace.MaintenanceProcedureProcess("procedure_process_001")
            proc2 = namespace.MaintenanceProcedureProcess("procedure_process_002")
            tool1 = namespace.Tool("tool_001")
            tool1.participantIn.append(proc2)
            tu.run_hermit_reasoner()
            result = tu.run_query(self.query)
            self.assertEqual(len(result), 0)
        namespace.destroy()


if __name__ == '__main__':
    unittest.main()

# <these tests are developed with the help of GitHub co-pilot>