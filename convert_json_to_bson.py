import json
import argparse
import os
import sys

try:
    import bson
except Exception as err:
    print("Module BSON is not found, please do a `pip install bson` to fix this error and rerun the things")
    sys.exit()


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--src-path", help = "Please point the path to json for the params to monitor")
    parser.add_argument("--target-file", help = "Please point the path to bson for the params to save as bson file")
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    print("Input Source path to parse and convert to the parameter" ,args.src_path)

    MODULE_BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(args.src_path)))
    ASSETS_FOLDER_PATH = os.path.join(MODULE_BASE_PATH, "assets")
    INPUT_FOLDER_PATH = os.path.join(MODULE_BASE_PATH, "input")

    MAVLINK_PARAMETERS_PATH = os.path.join(ASSETS_FOLDER_PATH, "parameters.json")

    TARGET_FILE_PATH = os.path.join(MODULE_BASE_PATH, "output", args.target_file)

    with open(MAVLINK_PARAMETERS_PATH) as mavlink_params_file:
        mavlink_params = json.load(mavlink_params_file).get("parameters", [])

    with open(args.src_path) as logging_params_file:
        logging_params = json.load(logging_params_file)

    with open(TARGET_FILE_PATH, mode = 'wb') as bson_file:
        bson_encode = bson.dumps(logging_params)
        bson_file.write(bson_encode)


if __name__ == '__main__':
    main()