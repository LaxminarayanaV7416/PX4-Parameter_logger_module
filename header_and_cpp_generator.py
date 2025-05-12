import json
import argparse
import os
import sys

try:
    from jinja2 import Environment, FileSystemLoader
except Exception as err:
    print("Failed to import jinja2: " + str(err))
    print("")
    print("You may need to install it using:")
    print("    pip3 install --user jinja2")
    print("")
    sys.exit(1)
    sys.exit()


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--src-path", help = "Please point the path to json for the params to monitor")
    parser.add_argument("--px4-base-path", help = "Please point the path to json for the params to monitor")
    parser.add_argument("--base-path", help = "Please point the base folder the program is located")
    parser.add_argument("--message-file-name", help = "Please enter the message file name")
    args = parser.parse_args()
    return args


def load_template(module_base_path, template_name):
    environment = Environment(loader=FileSystemLoader(os.path.join(module_base_path,"templates")))
    template = environment.get_template(template_name)
    return template

def convert_message_name_to_capitalized_camel_case(message_name):
    names = message_name.split("_")
    result = ""
    for name in names:
        result = f"{result}{name.capitalize()}".strip()
    return result

def alter_logger_cpp_file(px4_base_path, topic_name):
    file_path = os.path.join(px4_base_path, "src", "modules", "logger", "logged_topics.cpp")
    with open(file_path, mode = "r") as log_read:
        lines = log_read.readlines()
    writable_lines = []
    for line in lines:
        if "// multi topics" in line:
            writable_lines.append(f'\tadd_topic("{topic_name}", 100);\n')
        writable_lines.append(line)
    with open(file_path, mode= 'w') as log_file_writer:
        log_file_writer.writelines(writable_lines)

def add_config_logger_to_board(file_path, line):
    with open(file_path, mode = 'r') as file_buffer:
        lines = file_buffer.readlines()
    lines.append(line)
    with open(file_path, mode = 'w') as file_buffer:
        file_buffer.writelines(lines)


def main():
    args = get_args()
    print("Input Source path to parse and convert to the parameter" ,args.src_path)
    PX4_BASE_PATH = os.path.abspath(args.px4_base_path)
    MODULE_BASE_PATH = os.path.abspath(args.base_path)
    ASSETS_FOLDER_PATH = os.path.join(MODULE_BASE_PATH, "assets")
    MAVLINK_PARAMETERS_PATH = os.path.join(ASSETS_FOLDER_PATH, "parameters.json")

    with open(MAVLINK_PARAMETERS_PATH) as mavlink_params_file:
        mavlink_params = json.load(mavlink_params_file).get("parameters", [])

    with open(args.src_path) as input_file:
        input_params =  json.load(input_file).get("parameters", [])
        input_params = list(map(lambda inp : inp.lower(), input_params))

    params_data = {}
    for param_dict in mavlink_params:
        name = param_dict["name"].lower()
        if name in input_params:
            data_type = param_dict["type"].lower()
            params_data[name] = data_type

    # Geneating the parameter collector header file this will be inside the repo folder
    template = load_template(MODULE_BASE_PATH, "all_parameters_logger.h.jinja")
    content = template.render(params = params_data, message_file_name = args.message_file_name)

    with open(os.path.join(MODULE_BASE_PATH, "all_parameters_logger.h"), mode = 'w') as file_buffer:
        file_buffer.write(content)

    # Geneating the parameter collector cpp file this will be inside the repo folder
    template = load_template(MODULE_BASE_PATH, "all_parameters_logger.cpp.jinja")
    content = template.render(params = params_data,  message_file_name = args.message_file_name)

    with open(os.path.join(MODULE_BASE_PATH, "all_parameters_logger.cpp"), mode = 'w') as file_buffer:
        file_buffer.write(content)

    # Geneating the message file this will be inside the px4_base_folder/msg
    template = load_template(MODULE_BASE_PATH, "custom_message.msg.jinja")
    content = template.render(params = params_data)

    with open(os.path.join(PX4_BASE_PATH, "msg", f"{convert_message_name_to_capitalized_camel_case(args.message_file_name)}.msg"), mode = 'w') as file_buffer:
        file_buffer.write(content)

    # Geneating the CmakeLists.txt file this will be inside the px4_base_folder/msg
    template = load_template(MODULE_BASE_PATH, "CMakeLists.txt.jinja")
    content = template.render(custom_message_file_name = f"{convert_message_name_to_capitalized_camel_case(args.message_file_name)}.msg")

    with open(os.path.join(PX4_BASE_PATH, "msg", "CMakeLists.txt"), mode = 'w') as file_buffer:
        file_buffer.write(content)

    alter_logger_cpp_file(PX4_BASE_PATH, args.message_file_name)
    add_config_logger_to_board(
        os.path.join(PX4_BASE_PATH, "boards","px4", "sitl", "default.px4board"),
        f"CONFIG_EXAMPLES_PARAM_LOGGER=y\n"
    )
    add_config_logger_to_board(
        os.path.join(PX4_BASE_PATH, "ROMFS", "px4fmu_common", "init.d-posix", "rcS"),
        f"param_logger start\n"
    )

if __name__ == '__main__':
    main()
