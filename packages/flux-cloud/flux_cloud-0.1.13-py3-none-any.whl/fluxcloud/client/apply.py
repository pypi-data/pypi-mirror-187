# Copyright 2022 Lawrence Livermore National Security, LLC and other
# This is part of Flux Framework. See the COPYRIGHT file for details.
#
# SPDX-License-Identifier: Apache-2.0

import fluxcloud.utils as utils
from fluxcloud.main import get_experiment_client
from fluxcloud.main.experiment import ExperimentSetup

from .helpers import select_experiment


def main(args, parser, extra, subparser):
    utils.ensure_no_extra(extra)

    cli = get_experiment_client(args.cloud)
    setup = ExperimentSetup(
        args.experiments,
        force_cluster=args.force_cluster,
        template=args.template,
        cleanup=args.cleanup,
        outdir=args.output_dir,
        test=args.test,
        quiet=True,
    )

    # Update config settings on the fly
    cli.settings.update_params(args.config_params)
    setup.settings.update_params(args.config_params)
    experiment = select_experiment(setup, args.experiment_id, args.size)
    cli.apply(setup, experiment=experiment)
    setup.cleanup(setup.matrices)
