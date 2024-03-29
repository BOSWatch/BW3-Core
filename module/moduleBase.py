#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""!
    ____  ____  ______       __      __       __       _____
   / __ )/ __ \/ ___/ |     / /___ _/ /______/ /_     |__  /
  / __  / / / /\__ \| | /| / / __ `/ __/ ___/ __ \     /_ <
 / /_/ / /_/ /___/ /| |/ |/ / /_/ / /_/ /__/ / / /   ___/ /
/_____/\____//____/ |__/|__/\__,_/\__/\___/_/ /_/   /____/
                German BOS Information Script
                     by Bastian Schroll

@file:        moduleBase.py
@date:        01.03.2019
@author:      Bastian Schroll
@description: Module main class to inherit
"""
import logging
import time
from abc import ABC

from boswatch import wildcard

logging.debug("- %s loaded", __name__)


class ModuleBase(ABC):
    r"""!Main module class"""

    _modulesActive = []

    def __init__(self, moduleName, config):
        r"""!init preload some needed locals and then call onLoad() directly"""
        self._moduleName = moduleName
        self.config = config
        self._modulesActive.append(self)

        # for time counting
        self._cumTime = 0
        self._moduleTime = 0

        # for statistics
        self._runCount = 0
        self._moduleErrorCount = 0

        logging.debug("[%s] onLoad()", moduleName)
        self.onLoad()

    def _cleanup(self):
        r"""!Cleanup routine calls onUnload() directly"""
        logging.debug("[%s] onUnload()", self._moduleName)
        self._modulesActive.remove(self)
        self.onUnload()

    def _run(self, bwPacket):
        r"""!start an run of the module.

        @param bwPacket: A BOSWatch packet instance
        @return bwPacket or False"""
        self._runCount += 1
        logging.debug("[%s] run #%d", self._moduleName, self._runCount)

        tmpTime = time.time()
        try:
            logging.debug("[%s] doWork()", self._moduleName)
            bwPacket = self.doWork(bwPacket)
        except:
            self._moduleErrorCount += 1
            logging.exception("[%s] alarm error", self._moduleName)
        self._moduleTime = time.time() - tmpTime

        self._cumTime += self._moduleTime

        logging.debug("[%s] took %0.3f seconds", self._moduleName, self._moduleTime)

        return bwPacket

    def _getStatistics(self):
        r"""!Returns statistical information's from last module run

        @return Statistics as pyton dict"""
        stats = {"type": "module",
                 "runCount": self._runCount,
                 "cumTime": self._cumTime,
                 "moduleTime": self._moduleTime,
                 "moduleErrorCount": self._moduleErrorCount}
        return stats

    def onLoad(self):
        r"""!Called by import of the module
        can be inherited"""
        pass

    def doWork(self, bwPacket):
        r"""!Called module run
        can be inherited

        @param bwPacket: bwPacket instance"""
        logging.warning("no functionality in module %s", self._moduleName)

    def onUnload(self):
        r"""!Called on shutdown of boswatch
        can be inherited"""
        pass

    @staticmethod
    def registerWildcard(newWildcard, bwPacketField):
        r"""!Register a new wildcard

        @param newWildcard: wildcard where parser searching for
        @param bwPacketField: field from bwPacket where holds replacement data"""
        if not newWildcard.startswith("{") or not newWildcard.endswith("}"):
            logging.error("wildcard not registered - false format: %s", newWildcard)
            return
        if bwPacketField == "":
            logging.error("wildcard not registered - bwPacket field is empty")
            return
        wildcard.registerWildcard(newWildcard, bwPacketField)
