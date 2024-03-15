import unittest
import utility.TestUtilities as tu
import owlready2

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

    def test_base_case(self):

        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
                
        # arrage
        with namespace:
            proc1 = namespace.MaintenanceProcedureProcess("procedure_process_001")
            tool1 = namespace.Tool("tool_001")
            tool1.participantIn.append(proc1)

            tu.run_hermit_reasoner()

            # act
            result = tu.run_query(self.query)
            
            # assert that list has one entry
            self.assertEqual(len(result), 1)

            # assert that the resource found is the tool_001
            self.assertEqual(result[0][0], tool1)

        namespace.destroy()

    def test_multiple_resources(self):

        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
                
        # arrage
        with namespace:
            proc1 = namespace.MaintenanceProcedureProcess("procedure_process_001")
            tool1 = namespace.Tool("tool_001")
            tool2 = namespace.Tool("tool_002")
            tool1.participantIn.append(proc1)
            tool2.participantIn.append(proc1)

            tu.run_hermit_reasoner()

            # act
            result = tu.run_query(self.query)
            
            # assert that list has two entries
            self.assertEqual(len(result), 2)

            # assert that the resource found is the tool_001 and tool_0002
            self.assertTrue(tool1 in [x[0] for x in result])
            self.assertTrue(tool2 in [x[0] for x in result])

        namespace.destroy()

    def test_inheritance_reasoning_single_level(self):

        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")

        # arrange
        with namespace:
            proc1 = namespace.MaintenanceProcedureProcess("procedure_process_001")
            maintenance_task_1 = namespace.MaintenanceTask("maintenance_task_001")
            maintenance_task_1.directActivityPartOf.append(proc1)
            tool1 = namespace.Tool("tool_001")
            tool1.participantIn.append(maintenance_task_1)

            tu.run_hermit_reasoner()

            # act
            result = tu.run_query(self.query)

            # assert that list has one entry
            self.assertEqual(len(result), 1)
            
            # assert that the resource found is the tool_001
            self.assertEqual(result[0][0], tool1)

        namespace.destroy()

    # TODO: add swrl rules to ontology
            
    def test_inheritance_reasoning_multiple_levels(self):

        namespace = self.ontologies["spo"]

        # arrange
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

            # act
            result = tu.run_query(self.query)

            print("results")
            print(result)

            # assert that list has two entries
            self.assertEqual(len(result), 2)

            # assert that the resource found is the tool_001 and tool_002
            self.assertTrue(tool1 in [x[0] for x in result])
            self.assertTrue(tool2 in [x[0] for x in result])

        namespace.destroy()


if __name__ == '__main__':
    unittest.main()
