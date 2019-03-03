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

@file:        test_descriptor.py
@date:        07.01.2017
@author:      Bastian Schroll
@description: Unittests for BOSWatch. File have to run as "pytest" unittest
"""
import logging
import pytest

from module.descriptor import Descriptor
from module.descriptor import DescriptionList
from boswatch.packet import Packet


@pytest.mark.skip
class Test_Descriptor:
    """!Unittests for the descriptor"""

    def setup_method(self, method):
        logging.debug("[TEST] %s.%s", method.__module__, method.__name__)

    def test_loadCsvNotExist(self):
        """!read CSV file where not exist direct per DescriptionList class"""
        descList = DescriptionList()
        assert not descList.loadCSV("boswatch")

    def test_loadCsv(self):
        """!read CSV file direct per DescriptionList class"""
        descList = DescriptionList()
        assert descList.loadCSV("zvei")

    def test_descriptorLoadFailed(self):
        """!read CSV file where not exist"""
        bwDescriptor = Descriptor()
        assert not bwDescriptor.loadDescription("boswatch")

    def test_descriptorLoad(self):
        """!read CSV file"""
        bwDescriptor = Descriptor()
        assert bwDescriptor.loadDescription("zvei")

    def test_loadDescriptionsNotSet(self):
        """!load descriptions where not set to an bwPacket"""
        bwDescriptor = Descriptor()
        assert bwDescriptor.loadDescription("zvei")
        bwPacket = Packet()
        bwPacket.set("mode", "zvei")
        bwPacket.set("zvei", "54321")
        assert bwDescriptor.addDescriptions(bwPacket)
        assert bwPacket.get("shortDescription") is ""
        assert bwPacket.get("longDescription") is ""

    def test_loadDescriptions(self):
        """!load descriptions to an bwPacket"""
        bwDescriptor = Descriptor()
        assert bwDescriptor.loadDescription("zvei")
        bwPacket = Packet()
        bwPacket.set("mode", "zvei")
        bwPacket.set("zvei", "12345")
        assert bwDescriptor.addDescriptions(bwPacket)
        assert bwPacket.get("shortDescription") is not ""
        assert bwPacket.get("longDescription") is not ""
