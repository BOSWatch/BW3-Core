#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""!
    ____  ____  ______       __      __       __       _____
   / __ )/ __ \/ ___/ |     / /___ _/ /______/ /_     |__  /
  / __  / / / /\__ \| | /| / / __ `/ __/ ___/ __ \     /_ <
 / /_/ / /_/ /___/ /| |/ |/ / /_/ / /_/ /__/ / / /   ___/ /
/_____/\____//____/ |__/|__/\__,_/\__/\___/_/ /_/   /____/
                German BOS Information Script
                     by Bastian Schroll

@file:        header.py
@date:        11.12.2017
@author:      Bastian Schroll
@description: Prints the BOSWatch Header on Screen or logfile
"""
import logging
import platform  # for python version nr

from boswatch.utils import version

logging.debug("- %s loaded", __name__)


def logoToLog():
    r"""!Prints the BOSWatch logo to the log at debug level

    @return True or False on error"""
    logging.debug(r"    ____  ____  ______       __      __       __       _____ ")
    logging.debug(r"   / __ )/ __ \/ ___/ |     / /___ _/ /______/ /_     |__  / ")
    logging.debug(r"  / __  / / / /\__ \| | /| / / __ `/ __/ ___/ __ \     /_ <  ")
    logging.debug(r" / /_/ / /_/ /___/ /| |/ |/ / /_/ / /_/ /__/ / / /   ___/ /  ")
    logging.debug(r"/_____/\____//____/ |__/|__/\__,_/\__/\___/_/ /_/   /____/   ")
    logging.debug(r"                German BOS Information Script                ")
    logging.debug(r"                     by Bastian Schroll                      ")
    logging.debug(r"")
    return True


def infoToLog():
    r"""!Prints the BOSWatch and OS information to log at debug level

    @return True or False on error"""
    logging.debug("BOSWatch and environment information")
    logging.debug("- Client version:   %d.%d.%d",
                  version.client["major"],
                  version.client["minor"],
                  version.client["patch"])
    logging.debug("- Server version:   %d.%d.%d",
                  version.server["major"],
                  version.server["minor"],
                  version.server["patch"])
    logging.debug("- Branch:           %s",
                  version.branch)
    logging.debug("- Release date:     %02d.%02d.%4d",
                  version.date["day"],
                  version.date["month"],
                  version.date["year"])
    logging.debug("- Python version:   %s", platform.python_version())
    logging.debug("- Python build:     %s", platform.python_build())
    logging.debug("- System:           %s", platform.system())
    logging.debug("- OS Version:       %s", platform.platform())
    logging.debug("")
    return True
