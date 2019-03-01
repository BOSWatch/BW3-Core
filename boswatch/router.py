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
# todo think about implement threading for routers and the plugin calls (THREAD SAFETY!!!)
import logging
import copy
import importlib

logging.debug("- %s loaded", __name__)


class _Router:
    def __init__(self, name):
        self.__name = name
        self.__route = []
        logging.debug("[%s] new router", self.__name)

    def addRoute(self, route):
        logging.debug("[%s] add route: %s", self.__name, route)
        self.__route.append(route)

    def runRouter(self, bwPacket):
        logging.debug("[%s] started", self.__name)
        for routeCall in self.__route:
            logging.debug("[%s] -> run route: %s", self.__name, routeCall)
            bwPacket_tmp = routeCall(copy.deepcopy(bwPacket))  # copy bwPacket to prevent edit the original

            if bwPacket_tmp is None:  # returning None doesnt change the bwPacket
                continue

            if bwPacket_tmp is False:  # returning False stops the router immediately
                logging.debug("[%s] stopped", self.__name)
                break

            bwPacket = bwPacket_tmp
            logging.debug("[%s] <- bwPacket returned: %s", self.__name, bwPacket)
        logging.debug("[%s] ended", self.__name)
        return bwPacket

    @property
    def name(self):
        return self.__name

    @property
    def route(self):
        return self.__route


class RouterManager:
    def __init__(self):
        self.__routerDict = {}

    def __del__(self):
        del self.__routerDict

    def buildRouter(self, config):
        self.__routerDict = {}  # all routers and loaded modules/plugins would be unloaded
        logging.debug("build routers")

        # first we have to init all routers
        # because a router can be a valid target and we need his reference
        for router in config.get("router"):
            self.__routerDict[router.get("name")] = _Router(router.get("name"))

        for router in config.get("router"):
            for route in router.get("route"):

                routerName = router.get("name")
                routeType = route.get("type")
                routeName = route.get("name")

                if routeType is None or routeName is None:
                    logging.error("type or name error in config: %s", route)
                    continue

                try:
                    if routeType == "plugin":
                        importedFile = importlib.import_module(routeType + "." + routeName)
                        loadedClass = importedFile.BoswatchPlugin(route.get("config"))
                        self.__routerDict[routerName].addRoute(loadedClass._run)

                    elif routeType == "module":
                        importedFile = importlib.import_module(routeType + "." + routeName)
                        loadedClass = importedFile.BoswatchModule(route.get("config"))
                        self.__routerDict[routerName].addRoute(loadedClass._run)

                    elif routeType == "router":
                        self.__routerDict[routerName].addRoute(self.__routerDict[routeName].runRouter)

                    else:
                        logging.warning("unknown type: %s", routeType)

                except ModuleNotFoundError:
                    logging.error("%s not found: %s", route.get("type"), route.get("name"))
                    
        logging.debug("finished building routers")
        self._showRouterRoute()

    def runRouter(self, routerList, bwPacket):
        for router in routerList:
            if router in self.__routerDict:
                self.__routerDict[router].runRouter(bwPacket)

    def _showRouterRoute(self):
        for name, router in self.__routerDict.items():
            logging.debug("Route for %s", name)
            for route in router.route:
                logging.debug(" | %s", route)
