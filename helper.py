import glob
import json
import os
import shutil


def load_json(file_name):
    with open(file_name, 'r', encoding='UTF-8') as data_file:
        return json.load(data_file, strict=False)

def write_json(data, file_name):
    json_string = json.dumps(data, ensure_ascii=False)

    with open(file_name, 'w', encoding='UTF-8') as outfile:
        outfile.write(json_string)

def deleteDirsAndFiles(path_pattern):
    for fileOrDir in glob.glob(path_pattern):
        if os.path.isdir(fileOrDir):
            shutil.rmtree(fileOrDir)
        else:
            os.remove(fileOrDir)

