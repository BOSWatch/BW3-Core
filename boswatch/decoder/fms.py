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

@file:        fms.py
@date:        06.01.2018
@author:      Bastian Schroll
@description: Decoder class for fms
"""

import logging
import re

from boswatch.packet import packet

logging.debug("- %s loaded", __name__)


class Fms:
    """!FMS decoder class

    This class decodes FMS data.
    First step is to validate the data and _check if the format is correct.
    In the last step a valid BOSWatch packet is created and returned"""

    def __init__(self):
        """!Create a new instance"""
        logging.debug("FMS decoder started")

    @staticmethod
    def decode(data):
        """!Decodes FMS

        @param data: FMS for decoding
        @return BOSWatch FMS packet or None"""
        if "CRC correct" in data:
            service = data[19]
            country = data[36]
            location = data[61:63]
            vehicle = data[72:76]
            status = data[84]
            direction = data[101]
            directionText = data[103:110]
            tacticalInfo = data[114:117]
            fms_id = service + country + location + vehicle + status + direction

            if re.search("[0-9a-f]{8}[0-9a-f][01]", fms_id):
                logging.debug("found valid FMS")

                bwPacket = packet.Packet()
                bwPacket.set("mode", "fms")
                bwPacket.set("fms", fms_id)
                bwPacket.set("service", service)
                bwPacket.set("country", country)
                bwPacket.set("location", location)
                bwPacket.set("vehicle", vehicle)
                bwPacket.set("status", status)
                bwPacket.set("direction", direction)
                bwPacket.set("directionText", directionText)
                bwPacket.set("tacticalInfo", tacticalInfo)

                logging.debug(bwPacket)
                return bwPacket

            logging.warning("no valid data")
            return None
        logging.warning("CRC Error")
        return None
