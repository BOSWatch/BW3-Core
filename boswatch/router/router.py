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

logging.debug("- %s loaded", __name__)


class Router:
    """!Class for the Router"""
    def __init__(self, name):
        """!Create a new router

        @param name: name of the router"""
        self._name = name
        self._routeList = []
        logging.debug("[%s] new router", self._name)

    def addRoute(self, route):
        """!Adds a route point to the router

        @param route: instance of the Route class
        """
        logging.debug("[%s] add route: %s", self._name, route.name)
        self._routeList.append(route)

    def runRouter(self, bwPacket):
        """!Run the router

        @param bwPacket: instance of Packet class
        @return a instance of Packet class
        """
        logging.debug("[%s] started", self._name)
        for routeObject in self._routeList:
            logging.debug("[%s] -> run route: %s", self._name, routeObject)
            bwPacket_tmp = routeObject.callback(copy.deepcopy(bwPacket))  # copy bwPacket to prevent edit the original

            if bwPacket_tmp is None:  # returning None doesnt change the bwPacket
                continue

            if bwPacket_tmp is False:  # returning False stops the router immediately
                logging.debug("[%s] stopped", self._name)
                break

            bwPacket = bwPacket_tmp
            logging.debug("[%s] <- bwPacket returned: %s", self._name, bwPacket)
        logging.debug("[%s] ended", self._name)
        return bwPacket

    @property
    def name(self):
        """!Property to get the name of the router"""
        return self._name

    @property
    def routeList(self):
        """!Property to get a list of all route points of this router"""
        return self._routeList
