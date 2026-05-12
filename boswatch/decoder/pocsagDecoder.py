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

@file:        pocsagDecoder.py
@date:        15.10.2025
@author:      Bastian Schroll
@description: Decoder class for pocsag
"""

import logging
import re

from boswatch.packet import Packet

logging.debug("- %s loaded", __name__)


class PocsagDecoder:
    r"""!POCSAG decoder class

    This class decodes POCSAG data.
    First step is to validate the data and _check if the format is correct.
    In the last step a valid BOSWatch packet is created and returned"""

    @staticmethod
    def decode(data):
        r"""!Decodes POCSAG

        @param data: POCSAG for decoding
        @return BOSWatch POCSAG packet or None"""
        bitrate, ric, subric = PocsagDecoder._getBitrateRicSubric(data)

        # If no valid SubRIC (Function 0–3) detected → abort
        if subric is None:
            logging.warning("Invalid POCSAG function (not 0–3)")
            return None

        if ric and len(ric) == 7:
            if "Alpha:" in data:
                message = data.split('Alpha:')[1].strip()
                message = re.sub(r'<\s*(?:NUL|EOT)\s*>?', '', message).strip()
            else:
                message = ""
            subricText = subric.replace("1", "a").replace("2", "b").replace("3", "c").replace("4", "d")

            logging.debug("found valid POCSAG")

            bwPacket = Packet()
            bwPacket.set("mode", "pocsag")
            bwPacket.set("bitrate", bitrate)
            bwPacket.set("ric", ric)
            bwPacket.set("subric", subric)
            bwPacket.set("subricText", subricText)
            bwPacket.set("message", message)

            return bwPacket

        logging.warning("no valid POCSAG")
        return None

    @staticmethod
    def _getBitrateRicSubric(data):
        """Gets the Bitrate, Ric and Subric from data using robust regex parsing."""
        bitrate = "0"
        ric = None
        subric = None

        # determine bitrate
        if "POCSAG512:" in data:
            bitrate = "512"
        elif "POCSAG1200:" in data:
            bitrate = "1200"
        elif "POCSAG2400:" in data:
            bitrate = "2400"

        # extract RIC (address)
        m_ric = re.search(r'Address:\s*(\d{1,7})(?=\s|$)', data)
        if m_ric:
            ric = m_ric.group(1).zfill(7)

        # extract SubRIC (function)
        m_sub = re.search(r'Function:\s*([0-3])', data)
        if m_sub:
            subric = str(int(m_sub.group(1)) + 1)

        return bitrate, ric, subric
