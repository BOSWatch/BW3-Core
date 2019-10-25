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

@file:        routerManager.py
@date:        04.03.2019
@author:      Bastian Schroll
@description: Class for the BOSWatch packet router manager class
"""

# todo think about implement threading for routers and the plugin calls (THREAD SAFETY!!!)
import logging
import importlib
from boswatch.configYaml import ConfigYAML
from boswatch.router.router import Router
from boswatch.router.route import Route

logging.debug("- %s loaded", __name__)


class RouterManager:
    """!Class to manage all routers"""
    def __init__(self):
        """!Create new router"""
        self._routerDict = {}

    def __del__(self):
        """!Destroy the internal routerDict
        All routers and route point instances will be destroyed too
        Also destroys all instances from modules or plugins"""
        # destroy all routers (also destroys all instances of modules/plugins)
        del self._routerDict

    # if there is an error, router list would be empty (see tmp variable)
    def buildRouter(self, config):
        """!Initialize Routers from given config file

        @param config: instance of ConfigYaml class
        @return True or False"""
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
            routerDict_tmp[router.get("name")] = Router(router.get("name"))

        for router in config.get("router"):
            routerName = router.get("name")

            for route in router.get("route"):
                routeType = route.get("type")
                routeRes = route.get("res")
                routeName = route.get("name", default=routeRes)

                routeConfig = route.get("config", default=ConfigYAML())  # if no config - build a empty

                if routeType is None or routeRes is None:
                    logging.error("type or name not found in route: %s", route)
                    return False

                try:
                    if routeType == "plugin":
                        importedFile = importlib.import_module(routeType + "." + routeRes)
                        loadedClass = importedFile.BoswatchPlugin(routeConfig)
                        routerDict_tmp[routerName].addRoute(Route(routeName, loadedClass._run, loadedClass._getStatistics))

                    elif routeType == "module":
                        importedFile = importlib.import_module(routeType + "." + routeRes)
                        loadedClass = importedFile.BoswatchModule(routeConfig)
                        routerDict_tmp[routerName].addRoute(Route(routeName, loadedClass._run, loadedClass._getStatistics))

                    elif routeType == "router":
                        routerDict_tmp[routerName].addRoute(Route(routeName, routerDict_tmp[routeName].runRouter))

                    else:
                        logging.error("unknown type '%s' in %s", routeType, route)
                        return False

                # except ModuleNotFoundError:  # only since Py3.6
                except ImportError:
                    logging.error("%s not found: %s", route.get("type"), route.get("res"))
                    return False

        logging.debug("finished building routers")
        self._routerDict = routerDict_tmp
        self._showRouterRoute()
        return True

    def runRouters(self, routerRunList, bwPacket):
        """!Run given Routers

        @param routerRunList: string or list of router names in string form
        @param bwPacket: instance of Packet class"""
        if type(routerRunList) is str:  # convert single string name to list
            routerRunList = [routerRunList]

        for routerName in routerRunList:
            if routerName in self._routerDict:
                self._routerDict[routerName].runRouter(bwPacket)
            else:
                logging.warning("unknown router: %s", routerName)

    def _showRouterRoute(self):
        """!Show the routes of all routers"""
        for name, routerObject in self._routerDict.items():
            logging.debug("Route for %s", name)
            counter = 0
            for routePoint in routerObject.routeList:
                counter += 1
                logging.debug(" %d. %s", counter, routePoint.name)
