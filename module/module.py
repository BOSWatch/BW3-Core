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

@file:        module.py
@date:        01.03.2019
@author:      Bastian Schroll
@description: Module main class to inherit
"""
import logging
import time

logging.debug("- %s loaded", __name__)


class Module:
    """!Main module class"""

    _modulesActive = 0

    def __init__(self, moduleName, config):
        """!init preload some needed locals and then call onLoad() directly"""
        self._moduleName = moduleName
        self.config = config
        self._modulesActive += 1

        # for time counting
        self._cumTime = 0
        self._moduleTime = 0
        self._tmpTime = 0

        # for statistics
        self._runCount = 0
        self._moduleErrorCount = 0

        logging.debug("[%s] onLoad()", moduleName)
        self.onLoad()

    def __del__(self):
        """!Destructor calls onUnload() directly"""
        logging.debug("[%s] onUnload()", self._moduleName)
        self._modulesActive -= 1
        self.onUnload()

    def _run(self, bwPacket):
        """!start an rund of the module.

        @param bwPacket: A BOSWatch packet instance
        @return bwPacket or False"""
        self._runCount += 1
        logging.debug("[%s] run #%d", self._moduleName, self._runCount)

        self._tmpTime = time.time()
        try:
            logging.debug("[%s] doWork()", self._moduleName)
            bwPacket = self.doWork(bwPacket)
        except:
            self._moduleErrorCount += 1
            logging.exception("[%s] alarm error", self._moduleName)
        self._moduleTime = time.time() - self._tmpTime

        self._cumTime += self._moduleTime

        logging.debug("[%s] took %0.3f seconds", self._moduleName, self._moduleTime)

        return bwPacket

    def _getStatistics(self):
        """!Returns statistical information's from last module run

        @return Statistics as pyton dict"""
        stats = {"runCount": self._runCount,
                 "cumTime": self._cumTime,
                 "moduleTime": self._moduleTime,
                 "moduleErrorCount": self._moduleErrorCount}
        return stats

    def onLoad(self):
        """!Called by import of the module
        Must be inherit"""
        pass

    def doWork(self, bwPacket):
        """!Called module run
        Must be inherit

        @param bwPacket: bwPacket instance"""
        logging.warning("no functionality in module %s", self._moduleName)

    def onUnload(self):
        """!Called by destruction of the module
        Must be inherit"""
        pass
