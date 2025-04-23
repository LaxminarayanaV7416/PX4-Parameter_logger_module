import json
import argparse
import os
import sys

try:
    # import bson
    from jinja2 import Environment, FileSystemLoader
except Exception as err:
    print("Module BSON is not found, please do a `pip install bson` to fix this error and rerun the things")
    print("Failed to import jinja2 or bson: " + str(err))
    print("")
    print("You may need to install it using:")
    print("    pip3 install --user jinja2 bson")
    print("")
    sys.exit(1)
    sys.exit()


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--src-path", help = "Please point the path to json for the params to monitor")
    parser.add_argument("--base-path", help = "Please point the base folder the program is located")
    args = parser.parse_args()
    return args

def load_header_template(module_base_path):
    environment = Environment(loader=FileSystemLoader(os.path.join(module_base_path,"templates")))
    template = environment.get_template("all_parameters_logger.h.jinja")
    return template

def load_cpp_template(module_base_path):
    environment = Environment(loader=FileSystemLoader(os.path.join(module_base_path,"templates")))
    template = environment.get_template("all_parameters_logger.cpp.jinja")
    return template



def main():
    args = get_args()
    print("Input Source path to parse and convert to the parameter" ,args.src_path)

    MODULE_BASE_PATH = os.path.abspath(args.base_path)
    ASSETS_FOLDER_PATH = os.path.join(MODULE_BASE_PATH, "assets")
    MAVLINK_PARAMETERS_PATH = os.path.join(ASSETS_FOLDER_PATH, "parameters.json")

    with open(MAVLINK_PARAMETERS_PATH) as mavlink_params_file:
        mavlink_params = json.load(mavlink_params_file).get("parameters", [])

    with open(args.src_path) as input_file:
        input_params =  json.load(input_file).get("parameters", [])

    params_data = {}
    for param_dict in mavlink_params:
        name = param_dict["name"].lower()
        if name in input_params:
            data_type = param_dict["type"].lower()
            params_data[name] = data_type

    # with open(args.src_path) as logging_params_file:
    #     logging_params = json.load(logging_params_file)

    # with open(TARGET_FILE_PATH, mode = 'wb') as bson_file:
    #     bson_encode = bson.dumps(logging_params)
    #     bson_file.write(bson_encode)

    template = load_header_template(MODULE_BASE_PATH)
    content = template.render(params = params_data)

    with open(os.path.join(MODULE_BASE_PATH, "all_parameters_logger.h"), mode = 'w') as file_buffer:
        file_buffer.write(content)

    template = load_cpp_template(MODULE_BASE_PATH)
    content = template.render(params = params_data)

    with open(os.path.join(MODULE_BASE_PATH, "all_parameters_logger.cpp"), mode = 'w') as file_buffer:
        file_buffer.write(content)


if __name__ == '__main__':
    main()
