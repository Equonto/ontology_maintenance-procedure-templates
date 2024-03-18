import unittest
import utility.TestUtilities as tu
from owlready2 import *

'''
Competency ID: 07
User: Maintenance Engineer
Competency Question: I would like to know which procedures describe an end of life event for my equipment. Which of my procedures contain a "replacement" task?
'''
class TestOntologyCompetency7(unittest.TestCase):

    query = """
        prefix spo: <http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#>
        prefix iso: <http://rds.posccaesar.org/ontology/lis14/rdl/>

        SELECT DISTINCT ?procedure_process ?task ?text_value
        WHERE {
            ?task_description spo:hasTextValue ?text_value.
            ?task_description iso:isAbout ?task.
            ?task iso:activityPartOf ?procedure_process.
            ?procedure_process a spo:MaintenanceProcedureProcess
            FILTER (contains(str(?text_value),'replace'))
        } 
    """

    def setUp(self):
        tu.prepare_ontologies()
        self.ontologies = tu.load_ontology()

    def tearDown(self):
        self.ontologies = None
        tu.clear_staging()


    # TODO: finish when Media is in place


if __name__ == '__main__':
    unittest.main()

# <these tests are developed with the help of GitHub co-pilot>