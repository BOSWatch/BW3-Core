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
from boswatch.configYaml import ConfigYAML

logging.debug("- %s loaded", __name__)


class _Route:
    def __init__(self, name, callback):
        self._name = name
        self._callback = callback

    @property
    def name(self):
        return self._name

    @property
    def callback(self):
        return self._callback


class _Router:
    def __init__(self, name):
        self._name = name
        self._routeList = []
        logging.debug("[%s] new router", self._name)

    def addRoute(self, route):
        logging.debug("[%s] add route: %s", self._name, route.name)
        self._routeList.append(route)

    def runRouter(self, bwPacket):
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
        return self._name

    @property
    def routeList(self):
        return self._routeList


class RouterManager:
    def __init__(self):
        self._routerDict = {}

    def __del__(self):
        # destroy all routers (also destroys all instances of modules/plugins)
        del self._routerDict

    # if there is an error, router list would be empty (see tmp variable)
    def buildRouter(self, config):
        self._routerDict = {}  # all routers and instances of modules/plugins would be destroyed
        routerDict_tmp = {}
        logging.debug("build routers")

        # first we have to init all routers
        # because a router can be a valid target and we need his reference
        for router in config.get("router"):
            if router.get("name") is None or router.get("route") is None:
                logging.error("name or route not found in router: %s", router)
                return False
            if router.get("name") in self._routerDict:
                logging.error("duplicated router name: %s", router.get("name"))
                return False
            routerDict_tmp[router.get("name")] = _Router(router.get("name"))

        for router in config.get("router"):
            routerName = router.get("name")

            for route in router.get("route"):
                routeType = route.get("type")
                routeName = route.get("name")
                routeConfig = route.get("Config", default=ConfigYAML())  # if no config - build a empty

                if routeType is None or routeName is None:
                    logging.error("type or name not found in route: %s", route)
                    return False

                try:
                    if routeType == "plugin":
                        importedFile = importlib.import_module(routeType + "." + routeName)
                        loadedClass = importedFile.BoswatchPlugin(routeConfig)
                        routerDict_tmp[routerName].addRoute(_Route(routeName, loadedClass._run))

                    elif routeType == "module":
                        importedFile = importlib.import_module(routeType + "." + routeName)
                        loadedClass = importedFile.BoswatchModule(routeConfig)
                        routerDict_tmp[routerName].addRoute(_Route(routeName, loadedClass._run))

                    elif routeType == "router":
                        routerDict_tmp[routerName].addRoute(_Route(routeName, routerDict_tmp[routeName].runRouter))

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

    def runRouter(self, routerRunList, bwPacket):
        if type(routerRunList) is str:  # convert single string name to list
            routerRunList = [routerRunList]

        for routerName in routerRunList:
            if routerName in self._routerDict:
                self._routerDict[routerName].runRouter(bwPacket)

    def _showRouterRoute(self):
        for name, routerObject in self._routerDict.items():
            logging.debug("Route for %s", name)
            counter = 0
            for routePoint in routerObject.routeList:
                counter += 1
                logging.debug(" %d. %s", counter, routePoint.name)
