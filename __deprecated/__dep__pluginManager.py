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

@file:        pluginManager.py
@date:        08.01.2018
@author:      Bastian Schroll
@description: Plugin manager class to load and call the plugin
@todo must be mostly refactored
"""
import logging
import os
import time
import importlib

from boswatch import configYaml
from boswatch.utils import paths

logging.debug("- %s loaded", __name__)


class PluginManager:
    """!Plugin manager class to load, manage and call the plugin

    @todo refactor the class and add documentation"""

    def __init__(self):
        """!init comment"""
        self._config = configYaml.loadConfigSharepoint("serverConfig")
        self._pluginList = []

    def searchPluginDir(self):
        logging.debug("search for plugin in: %s", paths.PLUGIN_PATH)
        for name in os.listdir(paths.PLUGIN_PATH):
            location = os.path.join(paths.PLUGIN_PATH, name)

            # Skip if Path.isdir() or no File DIR_NAME.py is found
            if not os.path.isdir(location) or not name + ".py" in os.listdir(location):
                continue

            pluginPriority = self._config["plugin"][name]

            if pluginPriority is None:
                logging.warning("no entry in server config for plugin: %s", name)
                continue
            elif pluginPriority > 0:
                self._pluginList.append({"pluginName": name, "pluginPriority": pluginPriority})
                logging.debug("[ENABLED ] %s [%3d]", name, pluginPriority)
            elif pluginPriority <= 0:
                logging.debug("[DISABLED] %s ", name)

        # sort pluginList on pluginPriority descending (High to Low)
        self._pluginList.sort(key=lambda x: x['pluginPriority'], reverse=True)

    def importAllPlugins(self):
        logging.debug("importing all plugin")
        for item in self._pluginList:
            importPlugin = self._importPlugin(item["pluginName"])
            if importPlugin:
                item["pluginImport"] = importPlugin

    @staticmethod
    def _importPlugin(pluginName):
        logging.debug("import plugin: %s", pluginName)
        try:
            return importlib.import_module("plugin." + pluginName + "." + pluginName)
        except:
            logging.exception("error while loading plugin: %s", pluginName)
            return False

    def loadAllPlugins(self):
        logging.debug("loading all plugin")
        for item in self._pluginList:
            item["pluginObject"] = None  # todo del or none ???
            item["pluginObject"] = item["pluginImport"].BoswatchPlugin()

    def runAllPlugins(self, bwPacket):
        logging.info("ALARM - %0.3f sec. since radio reception", time.time() - bwPacket.get("timestamp"))
        for item in self._pluginList:
            item["pluginObject"]._run(bwPacket)
            item["pluginStatistics"] = item["pluginObject"]._getStatistics()
        self.printEndStats()

    def unloadAllPlugins(self):
        logging.debug("unload all plugin")
        for item in self._pluginList:
            #  todo del or None ???
            del item["pluginObject"]  # delete plugin object to force __del__() running

    def printEndStats(self):
        logging.debug("Plugin run statistics:")
        logging.debug("Plugin            | runs | tRUN |  tCUM  | tSET | tALA | tTRD | eSET | eALA | eTRD")
        for item in self._pluginList:
            logging.debug("- %-12s    | %4d | %0.2f | %6.1f | %0.2f | %0.2f | %0.2f | %4d | %4d | %4d",
                          item["pluginName"],
                          item["pluginStatistics"]["runCount"],
                          item["pluginStatistics"]["sumTime"],
                          item["pluginStatistics"]["cumTime"],
                          item["pluginStatistics"]["setupTime"],
                          item["pluginStatistics"]["alarmTime"],
                          item["pluginStatistics"]["teardownTime"],
                          item["pluginStatistics"]["setupErrorCount"],
                          item["pluginStatistics"]["alarmErrorCount"],
                          item["pluginStatistics"]["teardownErrorCount"])
