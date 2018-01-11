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


class Config:

    _sharePoints = {}

    def __init__(self):
        """!Create a new config object and load the ini file directly"""
        self._config = configparser.ConfigParser()

    def loadConfigFile(self, configPath, sharePoint=""):
        """!loads a given configuration in the class wide config variable

        @param configPath: Path to the config file
        @param sharePoint: If you like to share the config
        @return True or False"""
        logging.debug("load config file from: %s", configPath)
        try:
            self._config.read(configPath, "utf-8")
            if sharePoint:
                self._shareConfig(sharePoint)
            return True
        except:  # pragma: no cover
            logging.exception("cannot load config file")
            return False

    def _shareConfig(self, sharePoint):
        """!Shares the configuration

        Shares the local _config to teh class wide global _sharedConfig
        @param sharePoint: Name of the global share point
        @return True or False"""
        try:
            bool(self._sharePoints[sharePoint])
            logging.error("cannot share config - name is always in use: %s", sharePoint)
            return False
        except:
            self._sharePoints[sharePoint] = self._config
            logging.debug("configuration sharePoint: %s", sharePoint)
            return True

    def getInt(self, section, key, sharePoint=""):
        """!Method to read a single config entry as integer

        @param section: Section to read from
        @param key: Value to read
        @param sharePoint: Name of the global config share (empty is only local)
        @return The value or None"""
        value = self._get(section, key, sharePoint)
        if value is None:
            return int(0)
        return int(value)

    def getBool(self, section, key, sharePoint=""):
        """!Method to read a single config entry as boolean

        @param section: Section to read from
        @param key: Value to read
        @param sharePoint: Name of the global config share (empty is only local)
        @return The value or None"""
        return bool(self._get(section, key, sharePoint))

    def getStr(self, section, key, sharePoint=""):
        """!Method to read a single config entry as string

        @param section: Section to read from
        @param key: Value to read
        @param sharePoint: Name of the global config share (empty is only local)
        @return The value or None"""
        return str(self._get(section, key, sharePoint))

    def _get(self, section, key, sharePoint=""):
        """!Method to read a single config entry

        @param section: Section to read from
        @param key: Value to read
        @param sharePoint: Name of the global config share (empty is only local)
        @return The value or None"""
        if sharePoint:
            try:
                return self._sharePoints[sharePoint].get(section, key)
            except KeyError:
                logging.error("no sharePoint named: %s", sharePoint)
            except configparser.NoSectionError:
                logging.warning("no shared config section: %s", section)
            except configparser.NoOptionError:
                logging.warning("no shared config option: %s", key)
            except:  # pragma: no cover
                logging.exception("error while reading shared config")
            return None

        else:
            try:
                return self._config.get(section, key)
            except configparser.NoSectionError:
                logging.warning("no local config section: %s", section)
            except configparser.NoOptionError:
                logging.warning("no local config option: %s", key)
            except:  # pragma: no cover
                logging.exception("error while reading local config")
            return None

    def getAllSharepoints(self):
        """!Return a python dict of all set sharepoints

        @return Sharepoint dict"""
        return self._sharePoints
