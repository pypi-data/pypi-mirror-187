#!/usr/bin/python
#
# Copyright 2018-2023 Polyaxon, Inc.
# This file and its contents are licensed under the AGPLv3 License.
# Please see the included NOTICE for copyright information and
# LICENSE-AGPL for a copy of the license.
from haupt.common.test_cases.fixtures.bo import (
    get_fxt_bo_with_inputs_outputs,
    get_fxt_bo_with_run_patch,
)
from haupt.common.test_cases.fixtures.grid import get_fxt_grid_with_inputs_outputs
from haupt.common.test_cases.fixtures.jobs import (
    get_fxt_job,
    get_fxt_job_with_inputs,
    get_fxt_job_with_inputs_and_conditions,
    get_fxt_job_with_inputs_and_joins,
    get_fxt_job_with_inputs_outputs,
    get_fxt_tf_job,
)
from haupt.common.test_cases.fixtures.mapping import (
    get_fxt_mapping_with_inputs_outputs,
    get_fxt_mapping_with_run_patch,
)
from haupt.common.test_cases.fixtures.pipelines import (
    get_fxt_build_run_pipeline,
    get_fxt_build_run_pipeline_with_inputs,
    get_fxt_map_reduce,
    get_fxt_pipeline_params_env_termination,
    get_fxt_templated_pipeline_with_upstream_run,
    get_fxt_templated_pipeline_without_params,
    get_fxt_train_tensorboard_events_pipeline,
)
from haupt.common.test_cases.fixtures.schedule import (
    get_fxt_schedule_with_inputs_outputs,
)
from haupt.common.test_cases.fixtures.services import (
    get_fxt_job_with_hub_ref,
    get_fxt_service,
    get_fxt_service_with_inputs,
    get_fxt_service_with_upstream_runs,
)


def set_build_fixture(config, owner):
    config["build"] = {
        "params": {
            "context": {"value": "/path/context"},
        },
        "runPatch": {
            "init": [
                {
                    "git": {"revision": "branch2"},
                    "connection": "connection-repo",
                }
            ]
        },
        "hubRef": f"{owner}/kaniko",
    }
    return config
