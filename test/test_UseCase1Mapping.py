import unittest
import utility.TestUtilities as tu
from utility.UseCase1Mapper import UseCase1Mapper

'''
Tests Use Case 1 Mapping Against Competency Questions
'''
class TestUseCase1Mapping(unittest.TestCase):


    def setUp(self):
        self.ontologies = UseCase1Mapper().get_ontologies()

    def tearDown(self):
        self.ontologies = None
        tu.clear_staging()

    def test_useCaseMapping_competency1_shouldReturnNoResources(self):
        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            query = """
                prefix spo: <http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#>
                prefix iso: <http://rds.posccaesar.org/ontology/lis14/rdl/>

                SELECT ?resource
                WHERE {
                    VALUES ?procedure_process { spo:procedure_process_2M_mech_inspection } 
                    VALUES ?type { spo:Tool spo:Material spo:Permit } 
                    ?resource iso:participantIn ?procedure_process; a ?type 
                } 
            """     
            tu.run_pellet_reasoner()
            result = tu.run_query(query)
            self.assertEqual(len(result), 0)
        namespace.destroy()

    def test_useCaseMapping_competency2_shouldReturnTotalEightTasks(self):
        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            query = """
                prefix spo: <http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#>
                prefix iso: <http://rds.posccaesar.org/ontology/lis14/rdl/>

                SELECT ?maintenance_task ?parent
                WHERE {
                    VALUES ?procedure_process { spo:procedure_process_2M_mech_inspection  } 
                    ?maintenance_task iso:activityPartOf ?procedure_process .
                    ?maintenance_task spo:directActivityPartOf ?parent .
                }
            """     
            tu.run_pellet_reasoner()
            result = tu.run_query(query)
            self.assertEqual(len(result), 8)
        namespace.destroy()

    def test_useCaseMapping_competency3_shouldReturnLvl1Step2(self):
        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            query = """
                    prefix spo: <http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#>
                    prefix iso: <http://rds.posccaesar.org/ontology/lis14/rdl/>

                    SELECT ?next_maintenance_task ?media_type ?media_object_value ?media_object_location
                    WHERE {
                        VALUES ?current_maintenance_task { spo:lvl_1_task_1 } 
                        ?next_maintenance_task spo:directlyAfter ?current_maintenance_task .
                        OPTIONAL {
                            ?maintenance_task_description iso:isAbout ?next_maintenance_task .
                            ?maintenance_task_description iso:concretizedBy ?media_object .
                            ?media_object a ?media_type .
                            ?media_type rdfs:subClassOf spo:MediaObject .
                        }
                        OPTIONAL {
                            ?media_object spo:hasTextValue ?media_object_value .
                        }
                        OPTIONAL {
                            ?media_object spo:hasMediaLocation ?media_object_location .
                        }
                    }
            """     
            tu.run_pellet_reasoner()
            result = tu.run_query(query)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0][2], "Check that the suction & discharge piping are clear")
        namespace.destroy()

    def test_useCaseMapping_competency4_shouldReturnFourDocumentedHazards(self):
        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            query = """
                prefix spo: <http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#>
                prefix iso: <http://rds.posccaesar.org/ontology/lis14/rdl/>

                SELECT ?hazard
                WHERE {
                    VALUES ?procedure_process { spo:procedure_process_2M_mech_inspection }
                    ?hazard_realization_process iso:occursRelativeTo ?procedure_process .
                    ?hazard_realization_process iso:realizes ?hazard .
                    ?hazard a spo:Hazard 
                }
            """     
            tu.run_pellet_reasoner()
            result = tu.run_query(query)
            self.assertEqual(len(result), 4)
        namespace.destroy()


        
    def test_useCaseMapping_competency5_shouldReturnCorrectiveAction(self):

        spo = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        cmto = self.ontologies["cmto"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/conditional-maintenance-task-ontology#")

        with spo, cmto:

            query = """
                prefix spo: <http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#>
                prefix cmto: <http://spec.equonto.org/ontology/maintenance-procedure/conditional-maintenance-task-ontology#>
                prefix iso: <http://rds.posccaesar.org/ontology/lis14/rdl/>

                SELECT ?corrective_maintenance_task
                WHERE {
                    cmto:failure_1 cmto:addressedBy ?corrective_maintenance_task .
                    ?corrective_maintenance_task iso:activityPartOf spo:procedure_process_2M_mech_inspection; a cmto:CorrectiveMaintenanceTask .
                }
            """
            tu.run_pellet_reasoner()
            result = tu.run_query(query) 

            self.assertEqual(len(result), 1)
            self.assertEqual(result[0][0], cmto.CorrectiveMaintenanceTask("lvl_0_task_corrective_1"))
        
        spo.destroy()
        cmto.destroy()

    def test_useCaseMapping_competency6_shouldNotReturnProcedure(self):
        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
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
            tu.run_pellet_reasoner()
            result = tu.run_query(query)
            self.assertEqual(len(result), 0)

        namespace.destroy()

    def test_useCaseMapping_competency7(self):
        pass # todo: implement

    def test_useCaseMapping_competency8(self):
        pass # todo: implement

    def test_useCaseMapping_competency9_shouldReturnNoResources(self):
        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            query = """
                prefix spo: <http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#>
                prefix cmto: <http://spec.equonto.org/ontology/maintenance-procedure/conditional-maintenance-task-ontology#>
                prefix iso: <http://rds.posccaesar.org/ontology/lis14/rdl/>

                SELECT ?resource {
                VALUES ?procedure_process { spo:procedure_process_2M_mech_inspection } 
                ?resource iso:participantIn ?procedure_process; a spo:Resource
            }         
            """
            tu.run_pellet_reasoner()
            result = tu.run_query(query)
            self.assertEqual(len(result), 0)

        namespace.destroy()


if __name__ == '__main__':
    unittest.main()

# <these tests are developed with the help of GitHub co-pilot>