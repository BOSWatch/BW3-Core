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

@file:        plugin.py
@date:        08.01.2018
@author:      Bastian Schroll
@description: Plugin main class to inherit
"""
import logging
import time

logging.debug("- %s loaded", __name__)


class Plugin:
    """!Main plugin class"""

    _pluginsActive = 0

    def __init__(self, pluginName):
        """!init preload some needed locals
        and then call onLoad() directly"""
        self._pluginName = pluginName
        logging.debug("load %s", self._pluginName)
        self._pluginsActive += 1

        # for time counting
        self._setupTime = 0
        self._alarmTime = 0
        self._teardownTime = 0
        self._endTime = 0

        # for statistics
        self._runCount = 0
        self._setupErrorCount = 0
        self._alarmErrorCount = 0
        self._teardownErrorCount = 0

        self.onLoad()

    def __del__(self):
        """!Destructor calls onUnload() directly"""
        logging.debug("unload %s", self._pluginName)
        self._pluginsActive -= 1
        self.onUnload()

        logging.debug("[%s] statistics:", self._pluginName)
        logging.debug("- runs            %d", self._runCount)
        logging.debug("- setup errors    %d", self._setupErrorCount)
        logging.debug("- alarm errors    %d", self._alarmErrorCount)
        logging.debug("- teardown errors %d", self._teardownErrorCount)

    def _run(self, bwPacket):
        self._runCount += 1
        logging.debug("[%s] run #%s", self._pluginName, self._runCount)

        self._setupTime = time.time()
        try:
            logging.debug("[%s] setup", self._pluginName)
            self.setup()
        except:
            self._setupErrorCount += 1
            logging.exception("[%s] error in setup", self._pluginName)

        self._alarmTime = time.time()
        try:
            logging.debug("[%s] alarm", self._pluginName)
            self.alarm(bwPacket)
        except:
            self._alarmErrorCount += 1
            logging.exception("[%s] error in alarm", self._pluginName)

        self._teardownTime = time.time()
        try:
            logging.debug("[%s] teardown", self._pluginName)
            self.teardown()
        except:
            self._teardownErrorCount += 1
            logging.exception("[%s] error in teardown", self._pluginName)

        self._endTime = time.time()
        logging.debug("[%s] took %0.2f seconds", self._pluginName, self._endTime - self._setupTime)
        logging.debug("- setup:    %0.2f sec.", self._alarmTime - self._setupTime)
        logging.debug("- alarm:    %0.2f sec.", self._teardownTime - self._alarmTime)
        logging.debug("- teardown: %0.2f sec.", self._endTime - self._teardownTime)

    def onLoad(self):
        """!Called by import of the plugin
        Must be inherit"""
        pass

    def setup(self):
        """!Called before alarm
        Must be inherit"""
        pass

    def alarm(self, bwPacket):
        """!Called on alarm
        Must be inherit

        @param bwPacket: bwPacket instance"""
        pass

    def teardown(self):
        """!Called after alarm
        Must be inherit"""
        pass

    def onUnload(self):
        """!Called by destruction of the plugin
        Must be inherit"""
        pass
