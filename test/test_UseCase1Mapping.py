import unittest
import utility.TestUtilities as tu
from utility.UseCase1Mapper import UseCase1Mapper
import owlready2

'''
Tests Use Case 1 Mapping Against Competency Questions
'''
class UseCase1Mapping(unittest.TestCase):


    def setUp(self):
        tu.prepare_ontologies()
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

    # TODO: test failing because inverse in wrong direction.
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


if __name__ == '__main__':
    unittest.main()

# <these tests are developed with the help of GitHub co-pilot>