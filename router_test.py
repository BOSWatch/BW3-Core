#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from boswatch.configYaml import ConfigYAML
from boswatch.packet import Packet

import importlib
import copy


class Router:
    def __init__(self, name):
        self.__name = name
        self.__route = []
        logging.debug("add new router: %s", self.__name)

    def addRoute(self, route):
        logging.debug("[%s] add route: %s", self.__name, route)
        self.__route.append(route)

    def call(self, bwPacket):
        for call in self.__route:
            logging.debug("[%s] -> run route: %s", self.__name, call)
            bwPacket_tmp = call(copy.deepcopy(bwPacket))  # todo is deepcopy here right?

            if bwPacket_tmp is None:  # returning None doesnt change the bwPacket
                continue

            if bwPacket is False:  # returning False stops the router immediately
                logging.debug("[%s] stopped", self.__name)
                break

            bwPacket = bwPacket_tmp
            logging.debug("[%s] <- route returned: %s", self.__name, bwPacket)
        logging.debug("[%s] ended", self.__name)
        return bwPacket

    def showRoute(self):
        logging.debug("[%s] internal route", self.__name)
        for call in self.__route:
            logging.debug(" - %s", call)


config = ConfigYAML()
config.loadConfigFile("config/server.yaml")

routerList = {}
for router in config.get("router"):
    routerList[router.get("name")] = Router(router.get("name"))


for router in config.get("router"):
    for route in router.get("route"):

        if route.get("type") == "plugin":
            importedFile = importlib.import_module(route.get("type") + "." + route.get("name"))
            loadedClass = importedFile.BoswatchPlugin(route.get("config"))
            routerList[router.get("name")].addRoute(loadedClass._run)

        elif route.get("type") == "module":
            importedFile = importlib.import_module(route.get("type") + "." + route.get("name"))
            loadedClass = importedFile.BoswatchModule(route.get("config"))
            routerList[router.get("name")].addRoute(loadedClass._run)

        elif route.get("type") == "router":
            routerList[router.get("name")].addRoute(routerList[route.get("name")].call)

print()
print(routerList)
print()

for router in routerList:
    routerList[router].showRoute()

print()

bwPack = Packet("{'timestamp': 1551421020.9004176, 'mode': 'zvei', 'zvei': '12345'}")
for alaRouter in config.get("alarmRouter"):
    routerList[str(alaRouter)].call(bwPack)


#exit(0)
