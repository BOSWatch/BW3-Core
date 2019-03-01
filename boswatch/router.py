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
        self._name = name
        self._route = []
        logging.debug("[%s] new router", self._name)

    def addRoute(self, route):
        logging.debug("[%s] add route: %s", self._name, route)
        self._route.append(route)

    def runRouter(self, bwPacket):
        logging.debug("[%s] started", self._name)
        for routeCall in self._route:
            logging.debug("[%s] -> run route: %s", self._name, routeCall)
            bwPacket_tmp = routeCall(copy.deepcopy(bwPacket))  # copy bwPacket to prevent edit the original

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
        return self._name

    @property
    def route(self):
        return self._route


class RouterManager:
    def __init__(self):
        self._routerDict = {}

    def __del__(self):
        # destroy all routers (also destroys all instances of modules/plugins)
        del self._routerDict

    def buildRouter(self, config):  # todo validation
        self._routerDict = {}  # all routers and instances of modules/plugins would be destroyed
        routerDict_tmp = {}
        logging.debug("build routers")

        # first we have to init all routers
        # because a router can be a valid target and we need his reference
        for router in config.get("router"):
            if router.get("name") in self._routerDict:
                logging.error("duplicated router name: %s", router.get("name"))
                return False
            routerDict_tmp[router.get("name")] = _Router(router.get("name"))

        for router in config.get("router"):
            if router.get("name") is None or router.get("route") is None:
                logging.error("name or route not found in router: %s", router)
                return False

            for route in router.get("route"):

                routerName = router.get("name")
                routeType = route.get("type")
                routeName = route.get("name")

                if routeType is None or routeName is None:
                    logging.error("type or name not found in route: %s", route)
                    return False

                try:
                    if routeType == "plugin":
                        importedFile = importlib.import_module(routeType + "." + routeName)
                        loadedClass = importedFile.BoswatchPlugin(route.get("config"))
                        routerDict_tmp[routerName].addRoute(loadedClass._run)

                    elif routeType == "module":
                        importedFile = importlib.import_module(routeType + "." + routeName)
                        loadedClass = importedFile.BoswatchModule(route.get("config"))
                        routerDict_tmp[routerName].addRoute(loadedClass._run)

                    elif routeType == "router":
                        routerDict_tmp[routerName].addRoute(routerDict_tmp[routeName].runRouter)

                    else:
                        logging.error("unknown type '%s' in %s", routeType, route)
                        return False

                except ModuleNotFoundError:
                    logging.error("%s not found: %s", route.get("type"), route.get("name"))
                    return False

        logging.debug("finished building routers")
        self._routerDict = routerDict_tmp
        self._showRouterRoute()
        return True

    def runRouter(self, routerList, bwPacket):
        if type(routerList) is str:  # convert single string name to list
            routerList = [routerList]

        for routerName in routerList:
            if routerName in self._routerDict:
                self._routerDict[routerName].runRouter(bwPacket)

    def _showRouterRoute(self):
        for name, router in self._routerDict.items():
            logging.debug("Route for %s", name)
            for routePoint in router.route:
                logging.debug(" | %s", routePoint)
