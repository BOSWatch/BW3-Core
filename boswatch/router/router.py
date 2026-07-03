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

@file:        router.py
@date:        03.07.2026
@author:      Bastian Schroll, Claus Schichl
@description: Class for the BOSWatch packet router
"""
import logging
import copy
import time

logging.debug("- %s loaded", __name__)


class Router:
    r"""!Class for the Router"""
    def __init__(self, name):
        r"""!Create a new router

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
        r"""!Adds a route point to the router

        @param route: instance of the Route class
        """
        logging.debug("[%s] add route: %s", self.name, route.name)
        self.routeList.append(route)

    def runRouter(self, bwPacket):
        r"""!Run the router

        @param bwPacket: instance of Packet class
        @return an instance of Packet class, a list of packets, or False
        """
        self._runCount += 1
        tmpTime = time.time()

        logging.debug("[%s] started", self.name)

        # Start processing the route list recursively from index 0
        final_result = self._process_route_recursive(bwPacket, 0)

        logging.debug("[%s] finished", self.name)

        self._routerTime = time.time() - tmpTime
        self._cumTime += self._routerTime

        return final_result

    def _process_route_recursive(self, bwPacket, start_index):
        r"""!Recursively process the route to support list branching (e.g. for multicast)

        @param bwPacket: current packet to process
        @param start_index: index of the routeList to start from
        @return processed bwPacket, list of packets, or False
        """
        current_packet = bwPacket

        for i in range(start_index, len(self.routeList)):
            routeObject = self.routeList[i]
            logging.debug("[%s] -> run route: %s", self.name, routeObject.name)

            # State Isolation: pass a deep copy to prevent plugins from corrupting the RAM state of subsequent list items
            bwPacket_tmp = routeObject.callback(copy.deepcopy(current_packet))

            if bwPacket_tmp is None:
                # returning None doesnt change the current_packet
                continue

            if bwPacket_tmp is False:
                # returning False stops the route immediately for this specific packet branch
                logging.debug("[%s] stopped at route %s", self.name, routeObject.name)
                return False

            if isinstance(bwPacket_tmp, list):
                # Branching logic: A module returned a list of packets
                logging.debug("[%s] route %s returned a list. Branching for %d packets.", self.name, routeObject.name, len(bwPacket_tmp))
                results = []

                for single_packet in bwPacket_tmp:
                    # Recursively process the rest of the route (starting at next index) for each packet
                    res = self._process_route_recursive(single_packet, i + 1)

                    # Aggregate results
                    if res is not False and res is not None:
                        if isinstance(res, list):
                            results.extend(res)
                        else:
                            results.append(res)

                # The recursive calls already finished the rest of the route for all branches.
                # We return the aggregated results immediately to break out of this current loop level.
                return results if results else False

            # Normal single packet path: update the packet for the next iteration
            current_packet = bwPacket_tmp

        return current_packet

    def _getStatistics(self):
        r"""!Returns statistical information's from last router run

        @return Statistics as pyton dict"""
        stats = {"type": "router",
                 "runCount": self._runCount,
                 "cumTime": self._cumTime,
                 "moduleTime": self._routerTime}
        return stats
