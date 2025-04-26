# PX4-Parameter_logger_module
The Repository holds the module which basically logs the parameters to the ulog file


```{bash}
git submodule add https://github.com/LaxminarayanaV7416/PX4-Parameter_logger_module.git ./src/examples/param_logger
```

```{bash}
sudo chown -R $USER:$USER <path>/PX4-Autopilot
```

```{bash}
git submodule add https://github.com/LaxminarayanaV7416/PX4-Parameter_logger_module.git ./src/examples/param_logger
```

```{bash}
sudo git submodule update --init --recursive
```

make changes to the file <path>/PX4-Autopilot/boards/px4/sitl/default.px4board
add line `CONFIG_EXAMPLES_PARAM_LOGGER=y` at the last


to automatically start the things add line `param_logger start` to file rcS at path `<path>/PX4-Autopilot/ROMFS/px4fmu_common/init.d-posix/rcS`



To automatically start the param logging we need to add the last step that is starting the param_logger module at the start of the program for which we need to add the param_logger start command to the file called `<path>/PX4-Autopilot/ROMFS/px4fmu_common/init.d-posix/rcS` add the line `param_logger start` at the end of the file. then we are good to automatically start the logger to capture parameters logging automatically




`python3 header_and_cpp_generator.py --src-path ./input/monitoring_parameters.json --base-path .`



`python3 parameter_collector.py --base-path "/home/uavlab/Documents/PX4-Autopilot" --target-path .`

