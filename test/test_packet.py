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

@file:        test_packet.py
@date:        12.12.2017
@author:      Bastian Schroll
@description: Unittests for BOSWatch. File must be _run as "pytest" unittest
"""
import pytest
import logging

from boswatch.packet.packet import Packet


class Test_Packet:
    """!Unittests for the BOSWatch packet"""

    def setup_method(self, method):
        logging.debug("[TEST] %s.%s", (type(self).__name__, method.__name__))

    @pytest.fixture(scope="function")
    def buildPacket(self):
        """!Build a BOSWatch packet and serve it to each test"""
        bwPacket = Packet()
        yield bwPacket

    def test_createPacket(self):
        """!Create a packet"""
        bwPacket = Packet()
        assert bwPacket is not ""

    def test_copyPacket(self, buildPacket):
        """!Copy a packet to an new instance"""
        bwCopyPacket = Packet(buildPacket.__str__())
        assert bwCopyPacket is not ""

    def test_getPacketString(self, buildPacket):
        """!get the intern packet dict as string"""
        assert type(buildPacket.__str__()) is str
        assert buildPacket.__str__() is not ""

    def test_getNotSetField(self, buildPacket):
        """!try to get a not set field"""
        assert not buildPacket.get("testfield")

    def test_setGetField(self, buildPacket):
        """!set and get a field"""
        buildPacket.set("testField", "test")
        assert buildPacket.get("testField") is "test"

    def test_addClientData(self, buildPacket):
        """!add client data to packet"""
        buildPacket.addClientData()
        assert buildPacket.get("clientVersion")

    def test_addServerData(self, buildPacket):
        """!add server data to packet"""
        buildPacket.addServerData()
        assert buildPacket.get("serverVersion")
