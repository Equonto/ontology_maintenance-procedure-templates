
import utility.TestUtilities as ut

class UseCase1Mapper:

    def __init__(self):
        self.ontologies = self.load()

    def get_ontologies(self):
        return self.ontologies

    def load(self):
        ut.prepare_ontologies()
        return ut.load_ontology()

    def create_maintenance_procedure(self, document_name, procedure_title, process_name):
        spo = self.ontologies["spo"]
        document = spo.MaintenanceProcedureDocument(document_name)
        document.label.append(procedure_title)
        process = spo.MaintenanceProcedureProcess(process_name)
        document.isAbout.append(process)

    def create_maintainable_item(self, item_name, process_name):
        spo = self.ontologies["spo"]
        item = spo.MaintainableItem(item_name)
        process = spo.MaintenanceProcedureProcess(process_name)
        item.participantIn.append(process) # todo: might be has primary participant

    def create_hazard(self, hazard_name, process_name):
        spo = self.ontologies["spo"]
        hazard = spo.Hazard(hazard_name)
        process = spo.MaintenanceProcedureProcess(process_name)
        hazard_process = spo.HazardRealizationProcess(hazard_name + "_process")
        hazard.realizedIn.append(hazard_process)
        hazard_process.occursRelativeTo.append(process)

    def create_maintenance_task(self, task_name, task_type, parent_process_name, after_task_name, task_descriptions):  
        spo = self.ontologies["spo"]
        cmto = self.ontologies["cmto"]
        task = None
        if task_type == "required":
            task = spo.MaintenanceTask(task_name)
        if task_type == "corrective":
            task = cmto.CorrectiveMaintenanceTask(task_name)
        parent_process = spo.MaintenanceProcess(parent_process_name) # todo, check if this is alright
        parent_process.hasDirectActivityPart.append(task)
        if after_task_name:
            after_task = spo.MaintenanceTask(after_task_name)
            task.directlyAfter.append(after_task)

        for task_description in task_descriptions:
            task_description_instance = None
            if (task_description["task_description_type"] == "instructional"):
                task_description_instance = spo.InstructionalMaintenanceTaskDescription(task_description["task_description_name"])
            if (task_description["task_description_type"] == "auxilliary"):
                task_description_instance = spo.AuxilliaryMaintenanceTaskDescription(task_description["task_description_name"])

            for media in task_description["media"]:
                if (media["media_type"] == "text"):
                    text = spo.Text(media["media_name"])
                    text.hasTextValue.append(media["media_content"])
                    task_description_instance.concretizedBy.append(text)
                if (media["media_type"] == "image"):
                    image = spo.Image(media["media_name"])
                    image.hasMediaLocation.append(media["media_content"])
                    task_description_instance.concretizedBy.append(image)

    def create_failure(self, failure_name, natural_description, process_name):
        cmto = self.ontologies["cmto"]
        failure = cmto.FunctionalFailure(failure_name)
        failure.label.append(natural_description)
        failure.addressedBy.append(cmto.CorrectiveMaintenanceTask(process_name))

    def map(self):
        self.create_maintenance_procedure("procedure_document_2M_mech_inspection"
                                          , "2M Mech Insp Leak Detection Pumps"
                                          , "procedure_process_2M_mech_inspection")
        hazard_data = [
            { "hazard_name": "harm_to_persons_by_mechanical_impacts", "process_name": "procedure_process_2M_mech_inspection"}
           ,{ "hazard_name": "harm_to_persons_by_chemical_impacts", "process_name": "procedure_process_2M_mech_inspection"}
           ,{ "hazard_name": "harm_to_persons_by_electrical_impacts", "process_name": "procedure_process_2M_mech_inspection"}
           ,{ "hazard_name": "moving_parts_when_equipment_is_on", "process_name": "procedure_process_2M_mech_inspection"}
        ]

        for hazard in hazard_data:
            self.create_hazard(hazard["hazard_name"], hazard["process_name"])

        task_data = [
            { "task_name": "lvl_0_task_1",
                "task_type": "required",
                "parent_process_name": "procedure_process_2M_mech_inspection",
                "after_task_name": None,
                "task_descriptions": [{
                    "task_description_name": "lvl_0_task_1_description",
                    "task_description_type": "instructional",
                    "media": [
                        {"media_name":"lvl_0_task_1_description_media_1", "media_type": "text", "media_content": "Check that suction and discharge points are clear of obstruction and supply water to pump suction"}
                    ]
                },
                {
                    "task_description_name": "lvl_0_task_1_description_2",
                    "task_description_type": "auxilliary",
                    "media": [
                        {"media_name":"lvl_0_task_1_description_media_2", "media_type": "image", "media_content": "[schematic omitted]"}
                    ]
                }]
            },
            { "task_name": "lvl_1_task_1",
                "task_type": "required",
                "parent_process_name": "lvl_0_task_1",
                "after_task_name": None,
                "task_descriptions": [{
                    "task_description_name": "lvl_1_task_1_description",
                    "task_description_type": "instructional",
                    "media": [
                        {"media_name":"lvl_1_task_1_description_media_1", "media_type": "text", "media_content": "Check that the suction & discharge valves are clear"}
                    ]
                }]
            },
            { "task_name": "lvl_1_task_2",
             "task_type": "required", 
                "parent_process_name": "lvl_0_task_1",
                "after_task_name": "lvl_1_task_1",
                "task_descriptions": [{
                    "task_description_name": "lvl_1_task_2_description",
                    "task_description_type": "instructional",
                    "media": [
                        {"media_name":"lvl_1_task_2_description_media_1", "media_type": "text", "media_content": "Check that the suction & discharge piping are clear"}
                    ]
                }]
            },
            {
                "task_name": "lvl_1_task_3",
                "task_type": "required", 
                "parent_process_name": "lvl_0_task_1",
                "after_task_name": "lvl_1_task_2",
                "task_descriptions": [{
                    "task_description_name": "lvl_1_task_3_description",
                    "task_description_type": "instructional",
                    "media": [
                        {"media_name":"lvl_1_task_3_description_media_1", "media_type": "text", "media_content": "Look for any piping deformation or restriction"}
                    ]
                }]
            },
            { "task_name": "lvl_0_task_2",
              "task_type": "required",
                "parent_process_name": "procedure_process_2M_mech_inspection",
                "after_task_name": "lvl_0_task_1",
                "task_descriptions": [{
                    "task_description_name": "lvl_0_task_2_description",
                    "task_description_type": "instructional",
                    "media": [
                        {"media_name":"lvl_0_task_2_description_media_1", "media_type": "text", "media_content": "Look for any piping deformation or restriction."}
                    ]
                }]
            },
            {
                "task_name": "lvl_0_task_2",
                "task_type": "required",
                "parent_process_name": "procedure_process_2M_mech_inspection",
                "after_task_name": "lvl_0_task_1",
                "task_descriptions": [{
                    "task_description_name": "lvl_0_task_2_description",
                    "task_description_type": "instructional",
                    "media": [
                        {"media_name":"lvl_0_task_2_description_media_1", "media_type": "text", "media_content": "Check that the level in the leak detection tank [equipment id omitted] is enough to ensure NPSH in the pump suction."}
                    ]
                },
                {
                    "task_description_name": "lvl_0_task_2_description_2",
                    "task_description_type": "auxilliary",
                    "media": [
                        {"media_name":"lvl_0_task_2_description_media_2", "media_type": "image", "media_content": "[schematic omitted]"}
                    ]
                
                }]
            },
            {
                "task_name": "lvl_1_task_4",
                "task_type": "required",
                "parent_process_name": "lvl_0_task_2",
                "after_task_name": None,
                "task_descriptions": [{
                    "task_description_name": "lvl_1_task_4_description",
                    "task_description_type": "instructional",
                    "media": [
                        {"media_name":"lvl_1_task_4_description_media_1", "media_type": "text", "media_content": "Fill the tank with the storage water till the start-up setting level and check that the pump starts up"}
                    ]
                }]
            },
            {
                "task_name": "lvl_0_task_corrective_1",
                "task_type": "corrective",
                "parent_process_name": "procedure_process_2M_mech_inspection",
                "after_task_name": "lvl_0_task_1",
                "task_descriptions": []
            },
            {
                "task_name": "lvl_0_task_corrective_2",
                "task_type": "corrective",
                "parent_process_name": "procedure_process_2M_mech_inspection",
                "after_task_name": "lvl_0_task_2",
                "task_descriptions": []
            }
        ]

        for task in task_data:
            self.create_maintenance_task(task["task_name"], task["task_type"], task["parent_process_name"], task["after_task_name"], task["task_descriptions"])

        failure_data = [
            {
                "failure_name": "failure_1",
                "natural_description": "obstruction",
                "process_name": "lvl_0_task_corrective_1"
            },
            {
                "failure_name": "failure_2",
                "natural_description": "pump not starting when level is reached",
                "process_name": "lvl_0_task_corrective_2"
            }
        ]

        for failure in failure_data:
            self.create_failure(failure["failure_name"], failure["natural_description"], failure["process_name"])
