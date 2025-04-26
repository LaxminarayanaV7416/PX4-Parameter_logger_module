import json
import argparse
import os
import re
import pandas as pd
import enum

"""
There are totally four scenarios the parameters can come from
    - modules - straight forward from src > modules > <module_name> > *_params.c
    - lib - straight forward from src > lib > <lib_name> > *_params.c
    - drivers - not straight forward can have multiple folders in between src > drivers > <muliple FOLDERS> > *_params.c
    - build - straight forward from build > px4_* > generated_params > *_params.c
"""

class PathLocatorEnum(str, enum.Enum):
    src = "/src"
    build = "/build"

class TypeOfFolderEnum(str, enum.Enum):
    module = "modules"
    lib = "lib"
    driver = "drivers"

class TypeOfBuild(str, enum.Enum):
    sitl = "px4_sitl_default"
    v2 = "px4_fmu-v2_default"
    v4 = "px4_fmu-v4_default"
    v5 = "px4_fmu-v5_default"

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-path", help = "Please point the base folder the program is located")
    parser.add_argument("--target-path", help = "Please point the target file path to the save the file")
    args = parser.parse_args()
    return args

IGNORE_FOLDERS = ["examples", "templates", "systemcmds", "controllib_test"]
SUPPORTED_EXTENSIONS = [".c", ".cpp", ".h", ".hpp"]
DATASET_COLUMN_NAMES = ["param_name", "value", "datatype", "base_folder", 
                        "base_directory", "type", "type_name","file_path", "file_name"]
RE_PATTERNS = [
        { 
            "pattern" : re.compile(r'^PARAM_DEFINE_(?:INT32|FLOAT)\(\s*([^,]+)\s*,\s*([^)]+)\s*\);'),
            "group_count" : 2,
            "keys_to_use" : ["param_name", "value"]
        },
    ]
BASE_PATH = None

def file_opener(file_path):
    data = []
    try:
        with open(file= file_path, mode = 'r') as file_buffer:
            data = file_buffer.readlines()
    except Exception as err:
        print("something went wrong please check the error: ", err)
    return data

def file_path_decoupler(file_path):
    directory, file_name = os.path.split(file_path)
    directory = directory.rstrip("/")
    base_directory = directory.replace(BASE_PATH, "")
    typeof, type_name = "", ""
    if base_directory.startswith(PathLocatorEnum.src.value):
        base_directory = base_directory.lstrip(PathLocatorEnum.src.value)
        base_folder = PathLocatorEnum.src.value.strip("/")
        base_split = base_directory.split("/")
        if base_split[0] == TypeOfFolderEnum.module:
            typeof = TypeOfFolderEnum.module.value
            if len(base_split)>1:
                type_name = base_split[1]
        elif base_split[0] == TypeOfFolderEnum.lib:
            typeof = TypeOfFolderEnum.lib.value
            if len(base_split)>1:
                type_name = base_split[1]
        else:
            typeof = TypeOfFolderEnum.driver.value
            type_name = " >> ".join(base_split[1:])
    else:
        base_directory = base_directory.lstrip(PathLocatorEnum.build.value)
        base_folder = PathLocatorEnum.build.value.strip("/")
        base_split = base_directory.split("/")
        print(base_split)
        if base_split[0] == TypeOfBuild.sitl:
            typeof = TypeOfBuild.sitl.value
            if len(base_split)>1:
                type_name = base_split[1]
            print(typeof, type_name)
        elif base_split[0] == TypeOfBuild.v2:
            typeof = TypeOfBuild.v2.value
            if len(base_split)>1:
                type_name = base_split[1]
        elif base_split[0] == TypeOfBuild.v4:
            typeof = TypeOfBuild.v4.value
            if len(base_split)>1:
                type_name = base_split[1]
        elif base_split[0] == TypeOfBuild.v5:
            typeof = TypeOfBuild.v5.value
            if len(base_split)>1:
                type_name = base_split[1]
    return file_name, base_folder, base_directory, typeof, type_name


def extract_params(code_lines, file_path):
    data = []
    file_name, base_folder, base_directory, typeof, type_name = file_path_decoupler(file_path)
    for line in code_lines:
        line = line.strip().strip("\n")
        for pattern_data in RE_PATTERNS:
            pattern = pattern_data.get("pattern")
            group_count = pattern_data.get("group_count")
            keys_to_use = pattern_data.get("keys_to_use")
            match = pattern.match(line)
            if match:
                matched_data = dict.fromkeys(DATASET_COLUMN_NAMES)
                for match_number, key in zip(range(1, group_count+1), keys_to_use):
                    matched_value = match.group(match_number)
                    if matched_value.endswith("f") and key == "value":
                        matched_value = matched_value.strip("f")
                        matched_value = float(matched_value)
                        matched_data["datatype"] = "float"
                    elif key == "value":
                        matched_data["datatype"] = "int"
                    matched_data[key] = matched_value
                matched_data["file_path"] = file_path
                matched_data["file_name"] = file_name
                matched_data["base_folder"] = base_folder
                matched_data["type"] = typeof
                matched_data["type_name"] = type_name
                matched_data["base_directory"] = base_directory
                data.append(matched_data)
    return data


def folder_scrapper(base_path, data):
    folder_content = os.listdir(base_path)
    for file_name in folder_content:
        file_path = os.path.join(base_path,file_name)
        _, extension = os.path.splitext(file_name.lower())
        if os.path.isdir(file_path) and file_name not in IGNORE_FOLDERS:
            data = folder_scrapper(file_path, data)
        elif extension in SUPPORTED_EXTENSIONS:
            file_content = file_opener(file_path = file_path)
            data.extend(extract_params(file_content, file_path))
    return data


def main():
    args = get_args()
    global BASE_PATH
    BASE_PATH = os.path.abspath(args.base_path) #"/home/uavlab/Documents/PX4-Autopilot"
    data = []
    data = folder_scrapper(BASE_PATH, data)
    df = pd.DataFrame(data)
    TARGET_PATH = os.path.join(os.path.abspath(args.target_path), "parameters_metadata.csv")
    df.to_csv(TARGET_PATH, index = False)


if __name__ == "__main__":
    main()
    # BASE_PATH = "/home/uavlab/Documents/PX4-Autopilot"
    # print(file_path_decoupler("/home/uavlab/Documents/PX4-Autopilot/src/modules/qground_control/params.c"))
    # print(file_path_decoupler("/home/uavlab/Documents/PX4-Autopilot/build/px4_sitl_default/generated_params/serial_params.c"))