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

@file:        pocsag.py
@date:        06.01.2018
@author:      Bastian Schroll
@description: Decoder class for pocsag
"""

import logging
import re

from boswatch.packet import packet

logging.debug("- %s loaded", __name__)


class Pocsag:
    """!POCSAG decoder class

    This class decodes POCSAG data.
    First step is to validate the data and check if the format is correct.
    In the last step a valid BOSWatch packet is created and returned"""

    def __init__(self):
        """!Create a new instance"""
        logging.debug("POCSAG decoder started")

    @staticmethod
    def decode(self, data):
        """!Decodes POCSAG

        @param data: POCSAG for decoding
        @return BOSWatch POCSAG packet or None"""
        bitrate, ric, subric = Pocsag._getBitrateRicSubric(data)

        if re.search("[0-9]{7}", ric) and re.search("[1-4]{1}", subric):
            if "Alpha:" in data:
                message = data.split('Alpha:   ')[1].strip()
                message = message.replace('<NUL><NUL>', '').replace('<NUL>', '').replace('<NUL', '').replace('< NUL>', '').replace('<EOT>', '').strip()
            else:
                message = ""
            subricText = subric.replace("1", "a").replace("2", "b").replace("3", "c").replace("4", "d")

            logging.debug("found valid POCSAG")

            bwPacket = packet.Packet()
            bwPacket.setField("mode", "pocsag")
            bwPacket.setField("bitrate", bitrate)
            bwPacket.setField("ric", ric)
            bwPacket.setField("subric", subric)
            bwPacket.setField("subricText", subricText)
            bwPacket.setField("message", message)

            logging.debug(bwPacket)
            return bwPacket

        logging.warning("no valid data")
        return None

    @staticmethod
    def _getBitrateRicSubric(data):
        """!Gets the Bitrate, Ric and Subric from data

        @param data: POCSAG data string
        @return bitrate
        @return ric
        @return subric"""
        bitrate, ric, subric = 0, 0, 0

        if "POCSAG512:" in data:
            bitrate = 512
            ric = data[20:27].replace(" ", "").zfill(7)
            subric = str(int(data[39]) + 1)

        elif "POCSAG1200:" in data:
            bitrate = 1200
            ric = data[21:28].replace(" ", "").zfill(7)
            subric = str(int(data[40]) + 1)

        elif "POCSAG2400:" in data:
            bitrate = 2400
            ric = data[21:28].replace(" ", "").zfill(7)
            subric = str(int(data[40]) + 1)

        return bitrate, ric, subric
