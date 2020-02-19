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

@file:        router.py
@date:        01.03.2019
@author:      Bastian Schroll
@description: Class for the BOSWatch packet router
"""
import logging
import copy
import time

logging.debug("- %s loaded", __name__)


class Router:
    """!Class for the Router"""
    def __init__(self, name):
        """!Create a new router

        @param name: name of the router"""
        self.name = name
        self.routeList = []

        # for time counting
        self._cumTime = 0
        self._routerTime = 0

        # for statistics
        self._runCount = 0

        logging.debug("[%s] add new router", self.name)

    def addRoute(self, route):
        """!Adds a route point to the router

        @param route: instance of the Route class
        """
        logging.debug("[%s] add route: %s", self.name, route.name)
        self.routeList.append(route)

    def runRouter(self, bwPacket):
        """!Run the router

        @param bwPacket: instance of Packet class
        @return a instance of Packet class
        """
        self._runCount += 1
        tmpTime = time.time()

        logging.debug("[%s] started", self.name)

        for routeObject in self.routeList:
            logging.debug("[%s] -> run route: %s", self.name, routeObject.name)
            bwPacket_tmp = routeObject.callback(copy.deepcopy(bwPacket))  # copy bwPacket to prevent edit the original

            if bwPacket_tmp is None:  # returning None doesnt change the bwPacket
                continue

            if bwPacket_tmp is False:  # returning False stops the router immediately
                logging.debug("[%s] stopped", self.name)
                break

            bwPacket = bwPacket_tmp
            logging.debug("[%s] bwPacket returned", self.name)
        logging.debug("[%s] finished", self.name)

        self._routerTime = time.time() - tmpTime
        self._cumTime += self._routerTime

        return bwPacket

    def _getStatistics(self):
        """!Returns statistical information's from last router run

        @return Statistics as pyton dict"""
        stats = {"type": "router",
                 "runCount": self._runCount,
                 "cumTime": self._cumTime,
                 "moduleTime": self._routerTime}
        return stats
