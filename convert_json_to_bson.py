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
    TARGET_FILE_PATH = os.path.join(MODULE_BASE_PATH, args.target_file)

    # with open(MAVLINK_PARAMETERS_PATH) as mavlink_params_file:
    #     mavlink_params = json.load(mavlink_params_file).get("parameters", [])

    # with open(args.src_path) as logging_params_file:
    #     logging_params = json.load(logging_params_file)

    # with open(TARGET_FILE_PATH, mode = 'wb') as bson_file:
    #     bson_encode = bson.dumps(logging_params)
    #     bson_file.write(bson_encode)

    text = """
#pragma once

#include <px4_platform_common/app.h>
#include <px4_platform_common/module.h>
#include <px4_platform_common/module_params.h>
#include <uORB/Subscription.hpp>
#include <uORB/topics/parameter_update.h>
#include <parameters/param.h>

class AllParametersLogger : public ModuleBase<AllParametersLogger>, public ModuleParams
{
public:
    AllParametersLogger();

    ~AllParametersLogger() {}

    int main();

    static px4::AppState appState; /* track requests to terminate app */

private:
    // Subscription to parameter updates
    uORB::Subscription _param_sub{ORB_ID(parameter_update)};

    // Parameters to monitor (from local_position_estimator)
    param_t _lpe_fusion_param;
    param_t _lpe_acc_xy_param;
    param_t _lpe_acc_z_param;

    // Current values
    int32_t _lpe_fusion;
    float _lpe_acc_xy;
    float _lpe_acc_z;

    // // Check for parameter updates
    // void check_for_updates();

};


            """
    with open(os.path.join(MODULE_BASE_PATH, "all_parameters_logger.h"), mode = 'w') as file_buffer:
        file_buffer.write(text)


if __name__ == '__main__':
    main()
