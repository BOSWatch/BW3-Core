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
@description: Unittests for BOSWatch. File have to run as "pytest" unittest
"""
# problem of the pytest fixtures
# pylint: disable=redefined-outer-name
import logging
import pytest

from boswatch.packet import Packet


def setup_method(method):
    logging.debug("[TEST] %s.%s", method.__module__, method.__name__)


@pytest.fixture()
def buildPacket():
    """!Build a BOSWatch packet and serve it to each test"""
    return Packet()


def test_createPacket(buildPacket):
    """!Create a packet"""
    assert buildPacket != ""


def test_copyPacket(buildPacket):
    """!Copy a packet to an new instance"""
    bwCopyPacket = Packet(buildPacket.__str__())
    assert bwCopyPacket != ""


def test_getPacketString(buildPacket):
    """!get the intern packet dict as string"""
    assert type(buildPacket.__str__()) is str
    assert buildPacket.__str__() != ""


def test_getNotSetField(buildPacket):
    """!try to get a not set field"""
    assert not buildPacket.get("testfield")


def test_setGetField(buildPacket):
    """!set and get a field"""
    buildPacket.set("testField", "test")
    assert buildPacket.get("testField") == "test"
