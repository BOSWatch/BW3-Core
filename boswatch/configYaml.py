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
@description: Module for the configuration in YAML format
"""
import logging
import yaml

logging.debug("- %s loaded", __name__)


class ConfigYAML:

    def __init__(self, config=None):
        self.__config = config

    def __iter__(self):
        for item in self.__config:
            if type(item) is list or type(item) is dict:
                yield ConfigYAML(item)
            else:
                yield item

    def __str__(self):
        return str(self.__config)

    def loadConfigFile(self, configPath):
        """!loads a given configuration

        @param configPath: Path to the config file
        @return True or False"""
        logging.debug("load config file from: %s", configPath)
        try:
            with open(configPath) as file:
                # use safe_load instead load
                self.__config = yaml.safe_load(file)
            return True
        except:  # pragma: no cover
            logging.exception("cannot load config file")
            return False

    def get(self, *args, default=None):
        tmp = self.__config
        try:
            for arg in args:
                tmp = tmp.get(arg, default)
            if type(tmp) is list or type(tmp) is dict:
                return ConfigYAML(tmp)
            else:
                return tmp
        except AttributeError:
            return default
