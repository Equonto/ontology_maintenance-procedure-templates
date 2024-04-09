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
            ?text_class iso:concretizes ?task_description .
            ?text_class a spo:Text .
            ?text_class spo:hasTextValue ?text_value .
            ?task_description iso:isAbout ?task .
            ?task iso:activityPartOf ?procedure_process .
            ?procedure_process a spo:MaintenanceProcedureProcess .
            FILTER (contains(str(?text_value),'replace'))
        } 
    """

    def setUp(self):
        tu.prepare_ontologies()
        self.ontologies = tu.load_ontology()

    def tearDown(self):
        self.ontologies = None
        tu.clear_staging()


    def test_procedureContainsOneReplacementTask_shouldReturnProcedure(self):
        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            proc1 = namespace.MaintenanceProcedureProcess("procedure_process_001")
            task1 = namespace.MaintenanceTask("task_001")
            task1.directActivityPartOf.append(proc1)
            task1_description = namespace.MaintenanceTaskDescription("task_description_001")
            task1_description.isAbout.append(task1)
            task1_description_text = namespace.Text("task_description_text_001")
            task1_description_text.hasTextValue.append("replace impeller")
            task1_description_text.concretizes.append(task1_description)
            tu.run_pellet_reasoner()
            result = tu.run_query(self.query)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0][0], proc1)
            self.assertEqual(result[0][1], task1)
            self.assertEqual(result[0][2], "replace impeller")

        namespace.destroy()

    def text_procedureDoesNotContainReplacementTask_shouldNotReturnProcedure(self):
        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            proc1 = namespace.MaintenanceProcedureProcess("procedure_process_001")
            task1 = namespace.MaintenanceTask("task_001")
            task1.directActivityPartOf.append(proc1)
            task1_description = namespace.MaintenanceTaskDescription("task_description_001")
            task1_description.isAbout.append(task1)
            task1_description_text = namespace.Text("task_description_text_001")
            task1_description_text.hasTextValue.append("inspect impeller")
            task1_description_text.concretizes.append(task1_description)
            tu.run_pellet_reasoner()
            result = tu.run_query(self.query)
            self.assertEqual(len(result), 0)

    def text_multipleProceduresContainReplacementTask_shouldReturnAllRelevantProcedures(self):
        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            proc1 = namespace.MaintenanceProcedureProcess("procedure_process_001")
            proc2 = namespace.MaintenanceProcedureProcess("procedure_process_002")
            task1 = namespace.MaintenanceTask("task_001")
            task2 = namespace.MaintenanceTask("task_002")
            task1.directActivityPartOf.append(proc1)
            task2.directActivityPartOf.append(proc2)
            task1_description = namespace.MaintenanceTaskDescription("task_description_001")
            task2_description = namespace.MaintenanceTaskDescription("task_description_002")
            task1_description.isAbout.append(task1)
            task2_description.isAbout.append(task2)
            task1_description_text = namespace.Text("task_description_text_001")
            task2_description_text = namespace.Text("task_description_text_002")
            task1_description_text.hasTextValue.append("replace impeller")
            task2_description_text.hasTextValue.append("replace seal")
            task1_description_text.concretizes.append(task1_description)
            task2_description_text.concretizes.append(task2_description)
            tu.run_pellet_reasoner()
            result = tu.run_query(self.query)
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0][0], proc1)
            self.assertEqual(result[0][1], task1)
            self.assertEqual(result[0][2], "replace impeller")
            self.assertEqual(result[1][0], proc2)
            self.assertEqual(result[1][1], task2)
            self.assertEqual(result[1][2], "replace seal")
        namespace.destroy()

if __name__ == '__main__':
    unittest.main()

# <these tests are developed with the help of GitHub co-pilot>