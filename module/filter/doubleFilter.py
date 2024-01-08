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

@file:        doubleFilter.py
@date:        09.07.2020
@author:      Bastian Schroll, b-watch
@description: Filter module for double packages
"""
import logging
from module.moduleBase import ModuleBase

# ###################### #
# Custom plugin includes #
import time
# ######################

logging.debug("- %s loaded", __name__)


class BoswatchModule(ModuleBase):
    r"""!Description of the Module"""
    def __init__(self, config):
        r"""!Do not change anything here!"""
        super().__init__(__name__, config)  # you can access the config class on 'self.config'
        self._filterLists = {}
        logging.debug("Configured ignoreTime: %d", self.config.get("ignoreTime", default=10))
        logging.debug("Configured maxEntry: %d", self.config.get("maxEntry", default=10))

    def onLoad(self):
        r"""!Called by import of the plugin
        Remove if not implemented"""
        pass

    def doWork(self, bwPacket):
        r"""!start an run of the module.

        @param bwPacket: A BOSWatch packet instance"""
        if bwPacket.get("mode") == "fms":
            filterFields = ["fms"]
        elif bwPacket.get("mode") == "pocsag":
            filterFields = self.config.get("pocsagFields", default=["ric", "subric"])
        elif bwPacket.get("mode") == "zvei":
            filterFields = ["tone"]
        else:
            logging.error("No Filter for '%s'", bwPacket)
            return False

        if not bwPacket.get("mode") in self._filterLists:
            logging.debug("create new doubleFilter list for '%s'", bwPacket.get("mode"))
            self._filterLists[bwPacket.get("mode")] = []

        logging.debug("filterFields for '%s' is '%s'", bwPacket.get("mode"), ", ".join(filterFields))

        return self._check(bwPacket, filterFields)

    def onUnload(self):
        r"""!Called by destruction of the plugin
        Remove if not implemented"""
        pass

    def _check(self, bwPacket, filterFields):
        self._filterLists[bwPacket.get("mode")].insert(0, bwPacket)

        # delete entries that are to old
        counter = 0
        for listPacket in self._filterLists[bwPacket.get("mode")][1:]:  # [1:] skip first entry, thats the new one
            if float(listPacket.get("timestamp")) < (time.time() - self.config.get("ignoreTime", default=10)):
                self._filterLists[bwPacket.get("mode")].remove(listPacket)
                counter += 1
        if counter:
            logging.debug("%d old entry(s) removed", counter)

        # delete last entry if list is to big
        if len(self._filterLists[bwPacket.get("mode")]) > self.config.get("maxEntry", default=20):
            logging.debug("MaxEntry reached - delete oldest")
            self._filterLists[bwPacket.get("mode")].pop()

        for listPacket in self._filterLists[bwPacket.get("mode")][1:]:  # [1:] skip first entry, thats the new one
            if all(listPacket.get(x) == bwPacket.get(x) for x in filterFields):
                logging.debug("found duplicate: %s", bwPacket.get("mode"))
                return False

        logging.debug("doubleFilter ok")
        return None
