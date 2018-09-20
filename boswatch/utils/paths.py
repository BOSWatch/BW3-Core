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

@file:        paths.py
@date:        07.01.2018
@author:      Bastian Schroll
@description: Important paths for some functions
"""
import logging
import os
import sys
import platform

logging.debug("- %s loaded", __name__)

# note searching for root part is not a nice solution atm
ROOT_PATH = os.path.dirname(sys.modules['boswatch'].__file__).replace("\\", "/") + "/../"

# implements a system adaption for the paths
if platform.system() == "Linux":
    LOG_PATH = "/var/log/boswatch/"
else:
    LOG_PATH = ROOT_PATH + "log/"

CONFIG_PATH = ROOT_PATH + "config/"
PLUGIN_PATH = ROOT_PATH + "plugins/"
CSV_PATH = ROOT_PATH + "csv/"
BIN_PATH = ROOT_PATH + "_bin/"
TEST_PATH = ROOT_PATH + "test/"


def fileExist(filePath):
    return os.path.exists(filePath)


def makeDirIfNotExist(dirPath):
    """!Checks if an directory is existing and create it if not

    @param dirPath: Path of the directory
    @return Path of the directory or False"""
    try:
        if not os.path.exists(dirPath):
            os.mkdir(dirPath)
            logging.debug("directory created: %s", dirPath)
        return dirPath
    except:  # pragma: no cover
        logging.exception("error by creating a directory: %s", dirPath)
        return False
