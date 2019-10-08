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
import yaml.parser

logging.debug("- %s loaded", __name__)


class ConfigYAML:

    def __init__(self, config=None):
        self._config = config

    def __iter__(self):
        for item in self._config:
            if type(item) is list or type(item) is dict:
                yield ConfigYAML(item)
            else:
                yield item

    def __str__(self):
        """!Returns the string representation of the internal config dict"""
        return str(self._config)

    def loadConfigFile(self, configPath):
        """!loads a given configuration file

        @param configPath: Path to the config file
        @return True or False"""
        logging.debug("load config file from: %s", configPath)
        try:
            with open(configPath) as file:
                # use safe_load instead load
                self._config = yaml.safe_load(file)
            return True
        except FileNotFoundError:
            logging.error("config file not found: %s", configPath)
        except yaml.parser.ParserError:
            logging.exception("syntax error in config file: %s", configPath)
        return False

    def get(self, *args, default=None):
        """!Get a single value from the config
        or a value set in a new configYAML class instance

        @param *args: Config section (one ore more strings)
        @param default: Default value if section not found (None)
        @return: A single value, a value set in an configYAML instance, the default value"""
        tmp = self._config
        try:
            for arg in args:
                tmp = tmp.get(arg, default)
            if type(tmp) is list or type(tmp) is dict:
                return ConfigYAML(tmp)
            else:
                return tmp
        except AttributeError:
            return default
