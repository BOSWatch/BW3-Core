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

@file:        config.py
@date:        25.12.2017
@author:      Bastian Schroll
@description: Module for the configuration
"""
import logging
import configparser

logging.debug("- %s loaded", __name__)

_configFile = configparser.ConfigParser()


def loadConfig(configFile):
    """!loads a given configuration in the class wide config variable

    @param configFile: Path to the config file
    @return status of loading"""
    logging.debug("load config file from: %s", configFile)
    try:
        _configFile.read(configFile, "utf-8")
        return True
    except:  # pragma: no cover
        logging.exception("cannot load config file")
        return False


def getConfig(section, key):
    """!Method to read a single config entry

    @param section: Section to read from
    @param key: Value to read
    @return The value from config file"""
    try:
        return _configFile.get(section, key)
    except:  # pragma: no cover
        logging.exception("Error while reading a config entry")
        return None

#
#
#
#


class Config:

    _sharedConfig = {}

    def __init__(self, configPath="", shareName=""):
        """!Create a new config object and load the ini file directly

        @param configPath: Path to the ini file
        @param shareName: Name for the global share point (empty is only local)"""
        self._config = None
        self._loadConfigFile(configPath)
        if shareName:
            self._shareConfig(shareName)

    def _loadConfigFile(self, configPath):
        """!loads a given configuration in the class wide config variable

        @param configPath: Path to the config file
        @return status of loading"""
        logging.debug("load config file from: %s", configPath)
        try:
            self._config.read(configPath, "utf-8")
            return True
        except:  # pragma: no cover
            logging.exception("cannot load config file")
            return False

    def _shareConfig(self, shareName):
        """!Shares the configuration

        Shares the local _config to teh class wide global _sharedConfig
        @param shareName: Name of the global share point"""
        try:
            bool(self._sharedConfig[shareName])
            self._sharedConfig[shareName] = self._config
            logging.debug("shared configuration as: %s", shareName)
        except:
            logging.error("cannot share config because the name is always in use: %s", shareName)


    def getConfig(self, section, key, shareName=""):
        """!Method to read a single config entry

        @param section: Section to read from
        @param key: Value to read
        @param shareName: Name of the global config share (empty is only local)
        @return The value from config file"""
        try:
            if shareName:
                return self._sharedConfig[shareName].get(section, key)
            else:
                return self._config.get(section, key)
        except:  # pragma: no cover
            logging.exception("Error while reading a config entry")
            return None
