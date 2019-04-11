# coding: utf8
# Copyright (c) Marnik Bercx, University of Antwerp
# Distributed under the terms of the MIT License


import os
import shutil
import warnings

from fireworks import LaunchPad, FWorker
from fireworks.user_objects.queue_adapters.common_adapter import CommonAdapter

"""
Set of scripts for configuring the pybat package.
"""

__author__ = "Marnik Bercx"
__copyright__ = "Copyright 2018, Marnik Bercx, University of Antwerp"
__version__ = "pre-alpha"
__maintainer__ = "Marnik Bercx"
__email__ = "marnik.bercx@uantwerpen.be"
__date__ = "Mar 2019"


def launchpad(launchpad_file=None, database="base"):
    """
    Script to set up the configuration of the launchpad for accessing the workflow
    server.

    Args:
        launchpad_file (str): my_launchpad.yaml file from which to load the mongoDB database
            details.

    Returns:
        None

    """

    if launchpad_file:
        lpad = LaunchPad.from_file(launchpad_file)
    else:
        host = input("Please provide the server host: ")
        port = int(input("Please provide the port number: "))
        name = input("Please provide the server name: ")
        username = input("Please provide your username: ")
        password = input("Please provide your password: ")

        lpad = LaunchPad(
            host=host, port=port, name=name, username=username, password=password,
            ssl=True, authsource="admin"
        )
        # TODO Add server checks

    config_lpad_file = os.path.join(os.path.expanduser("~"), ".pybat_config",
                                    "launchpad", database + "_launchpad.yaml")
    try:
        os.makedirs(
            os.path.join(os.path.expanduser("~"), ".pybat_config", "launchpad")
        )
    except FileExistsError:
        pass

    lpad.to_file(config_lpad_file)


def fworker(fireworker_file=None, fworker_name="base"):
    """
    Script to set up the configuration of the fireworker.

    Returns:
        None

    """

    if fireworker_file:
        fireworker = FWorker.from_file(fireworker_file)
    else:
        name = input("Please provide the fireworker name: ")
        vasp_cmd = input("Please provide the full vasp command: ")
        fireworker = FWorker(name=name, category=["none", "1nodes"],
                             env={"vasp_cmd": vasp_cmd})

    try:
        os.makedirs(
            os.path.join(os.path.expanduser("~"), ".pybat_config", "fworker")
        )
    except FileExistsError:
        pass

    config_fw_file = os.path.join(os.path.expanduser("~"), ".pybat_config",
                                  "fworker", fworker_name + "_fworker.yaml")

    fireworker.to_file(config_fw_file)


def queue(qadapter_file, fworker_name="base"):
    """
    Script to set up the configuration of the queueing system. Note that we store the
    queue_adapter in the same configuration directory as the Fireworker, i.e. fworker.
    This is in the assumption that each worker has one preferred queueing system.

    Returns:
        None

    """

    try:
        os.makedirs(
            os.path.join(os.path.expanduser("~"), ".pybat_config", "fworker")
        )
    except FileExistsError:
        pass

    config_q_file = os.path.join(os.path.expanduser("~"), ".pybat_config",
                                 "fworker", fworker_name + "_qadapter.yaml")

    queue_adapter = CommonAdapter.from_file(qadapter_file)

    template_file = os.path.join(
        os.path.expanduser("~"), ".pybat_config", "fworker",
        fworker_name + "_job_template.sh"
    )
    if not os.path.exists(template_file):
        warnings.warn("No corresponding template file found. Don't forget to "
                      "use pybat config jobscript to add the template file of "
                      "the '" + fworker_name + "' fireworker.")

    queue_adapter.template_file = template_file
    queue_adapter.to_file(config_q_file)


def jobscript(template_file, fworker_name="base"):
    """
    Add a template jobscript for submitting jobs to a queueing system. Should be
    adaptable by a queue_adapter, i.e. it should contain variable such as $${nnodes},
    $${rocket_launch}, etc... Again, we'll assume for now that one template per
    fireworker is sufficient.

    Args:
        template_file:
        fworker_name:

    Returns:

    """

    try:
        os.makedirs(
            os.path.join(os.path.expanduser("~"), ".pybat_config", "fworker")
        )
    except FileExistsError:
        pass

    config_template_file = os.path.join(os.path.expanduser("~"), ".pybat_config",
                                        "fworker", fworker_name + "_job_template.sh")

    shutil.copy(template_file, config_template_file)

def load_config(config, name="base"):
    """

    Args:
        config:
        name:

    Returns:

    """
    if config == "launchpad":
        return LaunchPad.from_file(
            os.path.join(os.path.expanduser("~"), ".pybat_config",
                         "launchpad", name + "_launchpad.yaml")
        )
    if config == "fworker":
        return FWorker.from_file(
            os.path.join(os.path.expanduser("~"), ".pybat_config",
                         "fworker", name + "_fworker.yaml")
        )
    if config == "qadapter":
        return CommonAdapter.from_file(
            os.path.join(os.path.expanduser("~"), ".pybat_config",
                         "fworker", name + "_qadapter.yaml")
        )