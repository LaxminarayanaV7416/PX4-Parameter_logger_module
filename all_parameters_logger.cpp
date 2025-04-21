/****************************************************************************
 *
 *   Copyright (C) 2025 UAV_LAB Development Team. All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in
 *    the documentation and/or other materials provided with the
 *    distribution.
 * 3. Neither the name PX4 nor the names of its contributors may be
 *    used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
 * FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
 * COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
 * BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
 * OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
 * AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
 * ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 *
 ****************************************************************************/

/**
 * @file all_parameters_logger.h
 * logs all parameters both local and global parameters based on the JSON file as input app for Linux
 *
 * @author Laxminarayana Vadnala <laxminarayana.vadnala@slu.edu>
 */


#include "all_parameters_logger.h"
#include <px4_platform_common/time.h>
#include <unistd.h>
#include <stdio.h>

px4::AppState AllParametersLogger::appState;

AllParametersLogger::AllParametersLogger() : ModuleParams(nullptr)
{
	// Find parameters by name
	_lpe_fusion_param = param_find("LPE_FUSION");
	_lpe_acc_xy_param = param_find("LPE_ACC_XY");
	_lpe_acc_z_param = param_find("LPE_ACC_Z");

	// Initialize values
	param_get(_lpe_fusion_param, &_lpe_fusion);
	param_get(_lpe_acc_xy_param, &_lpe_acc_xy);
	param_get(_lpe_acc_z_param, &_lpe_acc_z);
}

int AllParametersLogger::main()
{
	appState.setRunning(true);

	while (!appState.exitRequested()) {

		param_get(_lpe_fusion_param, &_lpe_fusion);
		param_get(_lpe_acc_xy_param, &_lpe_acc_xy);
		param_get(_lpe_acc_z_param, &_lpe_acc_z);

		PX4_INFO("Parameter Update:");
		PX4_INFO("LPE_FUSION: %" PRId32, _lpe_fusion);
		PX4_INFO("LPE_ACC_XY: %4.3f", static_cast<double>(_lpe_acc_xy));
		PX4_INFO("LPE_ACC_Z: %4.3f",  static_cast<double>(_lpe_acc_z));

		px4_sleep(2);
	}

	return 0;
}

