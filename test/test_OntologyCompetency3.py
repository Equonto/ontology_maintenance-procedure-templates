import unittest
import utility.TestUtilities as tu
from owlready2 import *

'''
Competency ID: 03
User: Maintenance Technician
Competency Question: Given that I am up to task x in a procedure, what tasks needs to be performed next.
'''
class TestOntologyCompetency3(unittest.TestCase):

    query = """
    prefix spo: <http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#>
    prefix iso: <http://rds.posccaesar.org/ontology/lis14/rdl/>

    SELECT ?next_maintenance_task ?media_type ?media_object_value ?media_object_location
    WHERE {
        VALUES ?current_maintenance_task { spo:task_001 } 
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

    def setUp(self):
        tu.prepare_ontologies()
        self.ontologies = tu.load_ontology()

    def tearDown(self):
        self.ontologies = None
        tu.clear_staging()

    def test_nextMaintenanceTaskExistsAtTopLevelWithMedia_shouldReturnNextMaintenanceTask(self):
        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            task1 = namespace.MaintenanceTask("task_001")
            task2 = namespace.MaintenanceTask("task_002")
            task2.directlyAfter.append(task1) 
            task2_description = namespace.MaintenanceTaskDescription("task_002_description")
            task2_description.isAbout.append(task2)
            task2_media = namespace.Text("media_object_001")
            task2_media.hasTextValue.append("replace tyres")
            task2_description.concretizedBy.append(task2_media)
            tu.run_pellet_reasoner()
            result = tu.run_query(self.query)
            res = result
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0][0], task2)
            self.assertEqual(result[0][1], namespace.Text)
            self.assertEqual(result[0][2], "replace tyres")
        namespace.destroy()

    def test_noNextMaintenanceTaskExists_shouldReturnEmptyList(self):
        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            task1 = namespace.MaintenanceTask("task_001")
            tu.run_pellet_reasoner()
            result = tu.run_query(self.query)
            self.assertEqual(len(result), 0)
        namespace.destroy()

    def test_mainenanceTaskExistsAtNestedLevel_shouldOnlyReturnItemsAtSameLevel(self):
        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            task1 = namespace.MaintenanceTask("task_001")
            task2 = namespace.MaintenanceTask("task_002")
            task2.directActivityPartOf.append(task1)
            tu.run_pellet_reasoner()
            result = tu.run_query(self.query)
            self.assertEqual(len(result), 0)
        namespace.destroy()

    def test_multipleSubsequentTasksExist_shouldOnlyReturnNextTask(self):
        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            task1 = namespace.MaintenanceTask("task_001")
            task2 = namespace.MaintenanceTask("task_002")
            task3 = namespace.MaintenanceTask("task_003")
            task2.directlyAfter.append(task1)
            task3.directlyAfter.append(task2)
            tu.run_pellet_reasoner()
            result = tu.run_query(self.query)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0][0], task2)
        namespace.destroy()

    def test_maintenanceTaskExistsWithMultipleMediaItems_shouldReturnAllMediaItems(self):
        namespace = self.ontologies["spo"].get_namespace("http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#")
        with namespace:
            task1 = namespace.MaintenanceTask("task_001")
            task2 = namespace.MaintenanceTask("task_002")
            task2.directlyAfter.append(task1)
            task2_description = namespace.MaintenanceTaskDescription("task_002_description")
            task2_description.isAbout.append(task2)
            task2_media1 = namespace.Text("media_object_001")
            task2_media1.hasTextValue.append("replace tyres")
            task2_media2 = namespace.Image("media_object_002")
            task2_media2.hasMediaLocation.append("link to image of tyre")
            task2_description.concretizedBy.append(task2_media1)
            task2_description.concretizedBy.append(task2_media2)
            tu.run_pellet_reasoner()
            result = tu.run_query(self.query)
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0][0], task2)
            self.assertEqual(result[0][1], namespace.Text)
            self.assertEqual(result[0][2], "replace tyres")
            self.assertEqual(result[1][0], task2)
            self.assertEqual(result[1][1], namespace.Image)
            self.assertEqual(result[1][3], "link to image of tyre")
        namespace.destroy()

if __name__ == '__main__':
    unittest.main()


# <these tests are developed with the help of GitHub co-pilot>