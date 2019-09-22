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

@file:        packet.py
@date:        06.01.2018
@author:      Bastian Schroll
@description: Class for a BOSWatch data packet
"""
import logging
import time
from boswatch import version

logging.debug("- %s loaded", __name__)


class Packet:
    """!Class implementation of an BOSWatch packet"""

    def __init__(self, bwPacket=None):
        """!Build a new BOSWatch packet or copy existing data in it

        @param bwPacket: Existing data to copy"""
        if bwPacket is None:
            logging.debug("create new bwPacket")
            self._packet = {"timestamp": time.time()}
        else:
            logging.debug("create bwPacket from string")
            self._packet = eval(str(bwPacket.strip()))

    def __str__(self):
        """!Return the intern _packet dict as string"""
        return str(self._packet)

    def set(self, fieldName, value):
        """!Set a field in the intern _packet dict

        @param fieldName: Name of the data to set
        @param value: Value to set"""
        self._packet[fieldName] = value

    def get(self, fieldName):
        """!Returns the value from a single field.
        If field not existing `None` is returned

        @param fieldName: Name of the field
        @return Value or None"""
        try:
            return self._packet[fieldName]
        except:
            logging.warning("field not found: %s", fieldName)
            return None

    def addClientData(self, config):
        """!Add the client information to the decoded data

        This function adds the following data to the bwPacket:
        - clientName
        - clientVersion
        - clientBuildDate
        - clientBranch
        - inputSource
        - frequency"""
        logging.debug("add client data to bwPacket")
        self.set("clientName", config.get("client", "name"))
        self.set("clientVersion", version.client)
        self.set("clientBuildDate", version.date)
        self.set("clientBranch", version.branch)
        self.set("inputSource", config.get("client", "inputSource"))
        self.set("frequency", config.get("inputSource", "sdr", "frequency"))

    def addServerData(self, config):
        """!Add the server information to the decoded data

        This function adds the following data to the bwPacket:
        - serverName
        - serverVersion
        - serverBuildDate
        - serverBranch"""
        logging.debug("add server data to bwPacket")
        self.set("serverName", config.get("server", "name"))
        self.set("serverVersion", version.server)
        self.set("serverBuildDate", version.date)
        self.set("serverBranch", version.branch)

    def printInfo(self):
        """!Print a info message to the log on INFO level.
        Contains the most useful info about this packet.
        @todo not complete yet - must be edit to print nice formatted messages on console
        """
        logging.info("[%s]", self.get("mode"))