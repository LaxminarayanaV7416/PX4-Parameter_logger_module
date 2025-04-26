import json
import argparse
import os
import re
import pandas as pd

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--src-path", help = "Please point the path to json for the params to monitor")
    parser.add_argument("--base-path", help = "Please point the base folder the program is located")
    args = parser.parse_args()
    return args

IGNORE_FOLDERS = ["examples", "templates", "systemcmds", "controllib_test"]
SUPPORTED_EXTENSIONS = [".c", ".cpp", ".h", ".hpp"]
DATASET_COLUMN_NAMES = ["param_name", "value", "datatype", "file_path", "file_name"]
RE_PATTERNS = [
        { 
            "pattern" : re.compile(r'^PARAM_DEFINE_(?:INT32|FLOAT)\(\s*([^,]+)\s*,\s*([^)]+)\s*\);'),
            "group_count" : 2,
            "keys_to_use" : ["param_name", "value"]
        },
    ]

def file_opener(file_path):
    data = []
    try:
        with open(file= file_path, mode = 'r') as file_buffer:
            data = file_buffer.readlines()
    except Exception as err:
        print("something went wrong please check the error: ", err)
    return data

def extract_params(code_lines, file_path):
    data = []
    _, file_name = os.path.split(file_path)
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


if __name__ == "__main__":
    PATH = "/home/uavlab/Documents/PX4-Autopilot"
    # source_path = os.path.join(PATH, "src")
    data = []
    data = folder_scrapper(PATH, data)
    df = pd.DataFrame(data)
    df.to_csv("test.csv", index = False)


