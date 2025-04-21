############################################################################
#
#   Copyright (c) 2025 UAV_LAB development team. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name PX4 nor the names of its contributors may be
#    used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
# OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
# AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
############################################################################


# COMMAND ${PYTHON_EXECUTABLE} ${PX4_SOURCE_DIR}/src/examples/PX4-Parameter_logger_module/convert_json_to_bson.py
# 		--src-path `find ${PX4_SOURCE_DIR}/src -maxdepth 4 -type d` ${generated_params_dir}
# 		--inject-xml ${PX4_SOURCE_DIR}/src/lib/parameters/parameters_injected.xml
# 		--json ${PX4_BINARY_DIR}/docs/parameters.json
# 		--compress


px4_add_module(
	MODULE examples__param_logger
	MAIN param_logger
	COMPILE_FLAGS
	SRCS
        all_parameters_logger_px4_main.cpp
		all_parameters_logger_px4_start.cpp
		all_parameters_logger.cpp
	DEPENDS
	)
