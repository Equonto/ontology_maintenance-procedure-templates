# Python Lutra Runner

This is the documentation for the Python Lutra Runner.

### Prerequisites

You must have java installed on your computer to use this tool. On most windows machines, it will come pre-installed.

### How to run the tool

To run the tool, simply double-click the python-lutra-runner executable. This will open a command window that will show that the application is running. No further action is required here, just wait for the process to complete.

When the process is comple, a prompt will appear in the command window that says "Press Any Key to Exit". You can either press any key to stop the process or close the command window entirely.

### What does the tool do?

The tool uses the data files and OTTR templates in the config folder to produce an ontology. Once you have run the tool, and the ontology build process has completed, the produced ontology will appear in the `config/output` folder. 

WARNING: DO NOT EDIT THE ONTOLOGY IN THIS FILE DIRECTLY. If you do this, your changes will be overwritten the next time the tool is run. If you wish to edit the ontology, you mist edit the data files and / or the template files.

### How do I edit the ontology?

To add a class or an instance data to the ontology. You must use the data files located at `config/data`.

To update the structure of the ontology (i.e. to add a new axiom), the OTTR templates can be found in the `config/templates` folder.

Please note:
1. If you add columns to these files, the appropriate change must be made to the templates.
2. If you change prefixes in any of the files, the appropriate change must be made to the templates.
3. If you change the IRI of an entity in these files, make sure all references to this entity are also changed in the other files.
4. TEST the ontology regularly. This means:
   - Every time you make a change, you should run the tool and check your ontology. Do not spend 20 minues making changes without checking your ontology along the way.
   - Ensure that the ontology is checked and working before pushing any changes to datafiles or templates to GitHub.

### How do I change the file name of the ontology?

The filename of the ontology can be edited via `config/settings.json` file. This file can also be used to update the version number appearing in the filename.

