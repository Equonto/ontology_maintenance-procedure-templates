
import os
import glob
import shutil
import json

def clear_output_directory(folder_location):
    files = glob.glob(folder_location+"/*")
    for f in files:
        if os.path.isdir(f):
            shutil.rmtree(f)
        else:
            os.remove(f)

def move_files(src_folder, dst_folder):
    files = glob.glob(src_folder+"/*")
    for f in files:
        shutil.copy(f, dst_folder)

def read_json_file(file_path):
    with open(file_path, "r") as file:
        json_str = file.read()
    return json.loads(json_str)