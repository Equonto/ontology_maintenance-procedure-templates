import subprocess
import os

def run_lutra_process(ontology_filename, ontology_shortname):

    filenames = os.listdir("config/templates/bottr/"+ontology_shortname)
    full_filenames = ["templates/bottr/"+ontology_shortname+"/"+filename for filename in filenames]
    filenames_string = ' '.join(full_filenames)

    outputType = "wottr"
    outputFolder = "output/"
    outputFilename = ontology_filename
    libraryType = "stottr"
    libraryFolder = "templates/stottr"
    inputType = "bottr"
    inputFolder = filenames_string

    command = "java -jar lutra.jar -m expand -O " \
        + outputType + " -o " + outputFolder + outputFilename \
        + " -L " + libraryType + " -l " \
        + libraryFolder \
        + " -I " + inputType \
        + " " + inputFolder \
        + " --fetchMissing" \
        #+ " --quiet" \
    
    result = subprocess.run(command
        , stdout=subprocess.PIPE
        , stderr=subprocess.PIPE
        , shell=True
        , cwd="config")
        
    print(result.stderr.decode("utf-8"))
    
def run_docttr():

    command = "java -jar lutra.jar -m docttrLibrary -o output/docttr.html -L stottr -l templates/stottr --fetchMissing"

    result = subprocess.run(command
        , stdout=subprocess.PIPE
        , stderr=subprocess.PIPE
        , shell=True
        , cwd="config")
    
    print(result.stderr.decode("utf-8"))
