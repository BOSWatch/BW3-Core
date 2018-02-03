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

@file:        doubleFilter.py
@date:        15.01.2018
@author:      Bastian Schroll
@description: Class to implement a filter for double alarms
@todo test, refactor and document
@todo check_msg is not implemented yet
"""
import logging
import time

from boswatch.config import Config

logging.debug("- %s loaded", __name__)


class DoubleFilter:
    """!Double Filter Class"""

    def __init__(self):
        """!init"""
        self._config = Config()
        self._filterLists = {}

    def filter(self, bwPacket):

        if bwPacket.get("mode") is "fms":
            scanWord = "fms"
        elif bwPacket.get("mode") is "pocsag":
            scanWord = "ric"
        elif bwPacket.get("mode") is "zvei":
            scanWord = "zvei"
        else:
            logging.error("No Filter for '%s'", bwPacket)
            return False

        if not bwPacket.get("mode") in self._filterLists:
            logging.debug("create new doubleFilter list for '%s'", bwPacket.get("mode"))
            self._filterLists[bwPacket.get("mode")] = []

        # for debug
        print(len(self._filterLists[bwPacket.get("mode")]))

        logging.debug("scanWord for '%s' is '%s'", bwPacket.get("mode"), scanWord)

        return self.check(bwPacket, scanWord)

    def check(self, bwPacket, scanWord):
        self._filterLists[bwPacket.get("mode")].insert(0, bwPacket)

        # delete entrys that are to old
        counter = 0
        for listPacket in self._filterLists[bwPacket.get("mode")][1:]:  # [1:] skip first entry, thats the new one
            print(str(listPacket.get("timestamp")), str(time.time() - self._config.getInt("doubleFilter", "IgnoreTime", "serverConfig")))
            if listPacket.get("timestamp") < (time.time() - self._config.getInt("doubleFilter", "IgnoreTime", "serverConfig")):
                    self._filterLists[bwPacket.get("mode")].remove(listPacket)
                    counter += 1
        if counter:
            logging.debug("%d old entry(s) removed", counter)

        # delete last entry if list is to big
        if len(self._filterLists[bwPacket.get("mode")]) > self._config.getInt("doubleFilter", "MaxEntry", "serverConfig"):
            logging.debug("MaxEntry reached - delete oldest")
            self._filterLists[bwPacket.get("mode")].pop()

        for listPacket in self._filterLists[bwPacket.get("mode")][1:]:  # [1:] skip first entry, thats the new one
            if listPacket.get(scanWord) is bwPacket.get(scanWord):
                logging.debug("found duplicate: %s", bwPacket.get(scanWord))
                return False

        print("OK!")
        return True
