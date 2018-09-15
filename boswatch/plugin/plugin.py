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

from boswatch.utils import paths
from boswatch.config import Config
from boswatch.utils import wildcard

logging.debug("- %s loaded", __name__)


class Plugin:
    """!Main plugin class"""

    _pluginsActive = 0

    def __init__(self, pluginName):
        """!init preload some needed locals and then call onLoad() directly"""
        logging.debug("- %s loaded", pluginName)
        self._pluginName = pluginName
        self._pluginsActive += 1

        # to save the packet while alarm is running for other functions
        self._bwPacket = None

        # for time counting
        self._sumTime = 0
        self._cumTime = 0
        self._setupTime = 0
        self._alarmTime = 0
        self._teardownTime = 0
        self._tmpTime = 0

        # for statistics
        self._runCount = 0
        self._setupErrorCount = 0
        self._alarmErrorCount = 0
        self._teardownErrorCount = 0

        if paths.fileExist(paths.PLUGIN_PATH + pluginName + "/" + pluginName + ".ini"):
            self.config = Config()
            self.config.loadConfigFile(paths.PLUGIN_PATH + pluginName + "/" + pluginName + ".ini")
        else:
            logging.debug("no config for %s found", pluginName)

        logging.debug("[%s] onLoad()", pluginName)
        self.onLoad()

    def __del__(self):
        """!Destructor calls onUnload() directly"""
        logging.debug("[%s] onUnload()", self._pluginName)
        self._pluginsActive -= 1
        self.onUnload()

    def _run(self, bwPacket):
        """!start an complete running turn of an plugin.
        Calls setup(), alarm() and teardown() in this order.
        The alarm() method serves the BOSWatch packet to the plugin.

        @param bwPacket: A BOSWatch packet instance"""
        self._runCount += 1
        logging.debug("[%s] run #%d", self._pluginName, self._runCount)

        self._bwPacket = bwPacket

        self._tmpTime = time.time()
        try:
            logging.debug("[%s] setup()", self._pluginName)
            self.setup()
        except:
            self._setupErrorCount += 1
            logging.exception("[%s] error in setup()", self._pluginName)

        self._setupTime = time.time() - self._tmpTime
        self._tmpTime = time.time()
        try:

            if bwPacket.get("mode") is "fms":
                logging.debug("[%s] fms()", self._pluginName)
                self.fms(bwPacket)
            if bwPacket.get("mode") is "pocsag":
                logging.debug("[%s] pocsag()", self._pluginName)
                self.pocsag(bwPacket)
            if bwPacket.get("mode") is "zvei":
                logging.debug("[%s] zvei()", self._pluginName)
                self.zvei(bwPacket)
            if bwPacket.get("mode") is "msg":
                logging.debug("[%s] msg()", self._pluginName)
                self.msg(bwPacket)
        except:
            self._alarmErrorCount += 1
            logging.exception("[%s] alarm error", self._pluginName)

        self._alarmTime = time.time() - self._tmpTime
        self._tmpTime = time.time()
        try:
            logging.debug("[%s] teardown()", self._pluginName)
            self.teardown()
        except:
            self._teardownErrorCount += 1
            logging.exception("[%s] error in teardown()", self._pluginName)

        self._teardownTime = time.time() - self._tmpTime
        self._sumTime = self._setupTime + self._alarmTime + self._teardownTime
        self._cumTime += self._sumTime
        self._endTime = time.time()

        self._bwPacket = None

        logging.debug("[%s] took %0.3f seconds", self._pluginName, self._sumTime)
        # logging.debug("- setup:    %0.2f sec.", self._setupTime)
        # logging.debug("- alarm:    %0.2f sec.", self._alarmTime)
        # logging.debug("- teardown: %0.2f sec.", self._teardownTime)

    def _getStatistics(self):
        """!Returns statistical information's from last plugin run

        @return Statistics as pyton dict"""
        stats = {"runCount": self._runCount,
                 "sumTime": self._sumTime,
                 "cumTime": self._cumTime,
                 "setupTime": self._setupTime,
                 "alarmTime": self._alarmTime,
                 "teardownTime": self._teardownTime,
                 "setupErrorCount": self._setupErrorCount,
                 "alarmErrorCount": self._alarmErrorCount,
                 "teardownErrorCount": self._teardownErrorCount}
        return stats

    def onLoad(self):
        """!Called by import of the plugin
        Must be inherit"""
        pass

    def setup(self):
        """!Called before alarm
        Must be inherit"""
        pass

    def fms(self, bwPacket):
        """!Called on FMS alarm
        Must be inherit

        @param bwPacket: bwPacket instance"""
        logging.warning("ZVEI not implemented in %s", self._pluginName)

    def pocsag(self, bwPacket):
        """!Called on POCSAG alarm
        Must be inherit

        @param bwPacket: bwPacket instance"""
        logging.warning("POCSAG not implemented in %s", self._pluginName)

    def zvei(self, bwPacket):
        """!Called on ZVEI alarm
        Must be inherit

        @param bwPacket: bwPacket instance"""
        logging.warning("ZVEI not implemented in %s", self._pluginName)

    def msg(self, bwPacket):
        """!Called on MSG packet
        Must be inherit

        @param bwPacket: bwPacket instance"""
        logging.warning("MSG not implemented in %s", self._pluginName)

    def teardown(self):
        """!Called after alarm
        Must be inherit"""
        pass

    def onUnload(self):
        """!Called by destruction of the plugin
        Must be inherit"""
        pass

    def parseWildcards(self, msg):
        """!Return the message with parsed wildcards"""
        if self._bwPacket is None:
            logging.warning("wildcard replacing not allowed - no bwPacket set")
            return msg
        return wildcard.replaceWildcards(self._bwPacket, msg)
