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

@file:        zvei.py
@date:        05.01.2018
@author:      Bastian Schroll
@description: Decoder class for zvei
"""

import logging
import re

from boswatch.packet import Packet

logging.debug("- %s loaded", __name__)


class ZveiDecoder:
    """!ZVEI decoder class

    This class decodes ZVEI data.
    First step is to validate the data and _check if the format is correct.
    After that the double-tone-sign 'E' is replaced.
    In the last step a valid BOSWatch packet is created and returned"""

    @staticmethod
    def decode(data):
        """!Decodes ZVEI

        @param data: ZVEI for decoding
        @return BOSWatch ZVEI packet or None"""
        if re.search("[0-9E]{5}", data[7:12]):
            logging.debug("found valid ZVEI")

            bwPacket = Packet()
            bwPacket.set("mode", "zvei")
            bwPacket.set("tone", ZveiDecoder._solveDoubleTone(data[7:12]))

            return bwPacket

        logging.warning("no valid ZVEI")
        return None

    @staticmethod
    def _solveDoubleTone(data):
        """!Remove the doubleTone sign (here its the 'E')

        @param data: ZVEI for double tone sign replacement
        @return Double Tone replaced ZVEI"""
        if "E" in data:
            data_old = data
            for i in range(1, len(data)):
                if data[i] == "E":
                    data = data.replace("E", data[i - 1], 1)
            logging.debug("solve doubleTone: %s -> %s", data_old, data)
        return data
