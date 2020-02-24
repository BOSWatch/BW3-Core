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

@file:        geocoding.py
@date:        22.02.2020
@author:      Jan Speller
@description: Geocoding Module
"""
import logging
from module.moduleBase import ModuleBase

# ###################### #
# Custom plugin includes #
import geocoder
import re
# ###################### #

logging.debug("- %s loaded", __name__)


class BoswatchModule(ModuleBase):
    """!Description of the Module"""
    def __init__(self, config):
        """!Do not change anything here!"""
        super().__init__(__name__, config)  # you can access the config class on 'self.config'

    def doWork(self, bwPacket):
        """!start an run of the module.

        @param bwPacket: A BOSWatch packet instance"""
        if bwPacket.get("mode") == "pocsag":
            self.geocode(bwPacket)

        return bwPacket

    def geocode(self, bwPacket):
        """!find address in message and get latitude and longitude

        @param bwPacket: A BOSWatch packet instance"""
        try:
            addressArray = re.search(self.config.get("regex"), bwPacket.get("message"))
            provider = self.config.get("apiProvider")

            if addressArray[1] is None:
                logging.info("No address found, skipping geocoding")
                return bwPacket

            address = addressArray[1]
            bwPacket.set("address", address)
            self.registerWildcard("{ADDRESS}", "address")
            logging.info("Found address: '" + address + "' in packet")

            if "mapbox" == provider:
                logging.info("Using Mapbox as provider")
                g = geocoder.mapbox(address, key=self.config.get("apiToken"))
            elif "google" == provider:
                logging.info("Using Google as provider")
                g = geocoder.google(address, key=self.config.get("apiToken"))
            else:
                return bwPacket

            (lat, lon) = g.latlng
            logging.info("Found following coordinates for address: [lat=" + str(lat) + ", lon=" + str(lon) + "]")
            bwPacket.set("lat", lat)
            bwPacket.set("lon", lon)
            self.registerWildcard("{LAT}", "lat")
            self.registerWildcard("{LON}", "lon")

            return bwPacket
        except Exception as e:
            logging.exception("Unknown Error while executing geocoding module: " + str(type(e).__name__) + ": " + str(e))
        return bwPacket
