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

@file:        configYaml.py
@date:        27.02.2019
@author:      Bastian Schroll
@description: Module for the configuration in yaml format
"""
import logging
import yaml

logging.debug("- %s loaded", __name__)

__sharePoints = {}


def loadConfigFile(configPath, sharePoint=""):
    """!loads a given configuration

    @param configPath: Path to the config file
    @param sharePoint: If you want to share the config set name here
    @return python dict of config or None"""
    logging.debug("load config file from: %s", configPath)
    try:

        with open(configPath) as f:
            # use safe_load instead load
            config = yaml.safe_load(f)
        if sharePoint:
            _shareConfig(config, sharePoint)
        return config
    except:  # pragma: no cover
        logging.exception("cannot load config file")
        return None


def loadConfigSharepoint(sharePoint):
    """!loads a given configuration from an sharepoint

    @param sharePoint: Name of the sharepoint
    @return python dict of config or None"""
    try:
        return __sharePoints[sharePoint]
    except KeyError:
        logging.error("no sharePoint named: %s", sharePoint)
    except:  # pragma: no cover
        logging.exception("error while reading shared config")
    return None


def _shareConfig(config, sharePoint):
    """!Shares the configuration

    Shares the local _config to the class wide global _sharedConfig
    @param config: Python dict of the configuration
    @param sharePoint: Name of the global share point
    @return True or False"""
    if sharePoint in __sharePoints:
        logging.error("cannot share config - name is always in use: %s", sharePoint)
        return False
    else:
        __sharePoints[sharePoint] = config
        logging.debug("add config sharePoint: %s", sharePoint)
        return True


def getAllSharepoints():
    """!Return a python dict of all set sharepoints

    @return Sharepoint dict"""
    return __sharePoints
