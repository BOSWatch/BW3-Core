#!/usr/bin/python
# -*- coding: utf-8 -*-
"""!
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

import boswatch.version

logging.debug("- %s loaded", __name__)


def logoToLog():
    """!Prints the BOSWatch logo to the log at debug level

    @return True or False on error"""
    try:
        logging.debug("    ____  ____  ______       __      __       __       _____ ")
        logging.debug("   / __ )/ __ \/ ___/ |     / /___ _/ /______/ /_     |__  / ")
        logging.debug("  / __  / / / /\__ \| | /| / / __ `/ __/ ___/ __ \     /_ <  ")
        logging.debug(" / /_/ / /_/ /___/ /| |/ |/ / /_/ / /_/ /__/ / / /   ___/ /  ")
        logging.debug("/_____/\____//____/ |__/|__/\__,_/\__/\___/_/ /_/   /____/   ")
        logging.debug("                German BOS Information Script                ")
        logging.debug("                     by Bastian Schroll                      ")
        logging.debug("")
        return True
    except:  # pragma: no cover
        logging.exception("cannot display logo in log")
        return False


def infoToLog():
    """!Prints the BOSWatch and OS information to log at debug level

    @return True or False on error"""
    try:
        logging.debug("BOSWatch and environment information")
        logging.debug("- Client version:   %d.%d.%d",
                      boswatch.version.client["major"],
                      boswatch.version.client["minor"],
                      boswatch.version.client["patch"])
        logging.debug("- Server version:   %d.%d.%d",
                      boswatch.version.server["major"],
                      boswatch.version.server["minor"],
                      boswatch.version.server["patch"])
        logging.debug("- Branch:           %s",
                      boswatch.version.branch)
        logging.debug("- Release date:     %02d.%02d.%4d",
                      boswatch.version.date["day"],
                      boswatch.version.date["month"],
                      boswatch.version.date["year"])
        logging.debug("- Python version:   %s", platform.python_version())
        logging.debug("- Python build:     %s", platform.python_build())
        logging.debug("- System:           %s", platform.system())
        logging.debug("- OS Version:       %s", platform.platform())
        logging.debug("")
        return True
    except:  # pragma: no cover
        logging.exception("cannot display OS information")
        return False


def logoToScreen():
    """!Prints the BOSWatch logo to the screen at debug level

    @return True or False on error"""
    try:
        print("    ____  ____  ______       __      __       __       _____ ")
        print("   / __ )/ __ \/ ___/ |     / /___ _/ /______/ /_     |__  / ")
        print("  / __  / / / /\__ \| | /| / / __ `/ __/ ___/ __ \     /_ <  ")
        print(" / /_/ / /_/ /___/ /| |/ |/ / /_/ / /_/ /__/ / / /   ___/ /  ")
        print("/_____/\____//____/ |__/|__/\__,_/\__/\___/_/ /_/   /____/   ")
        print("                German BOS Information Script                ")
        print("                     by Bastian Schroll                      ")
        print("")
        return True
    except:  # pragma: no cover
        logging.exception("cannot display logo on screen")
        return False
