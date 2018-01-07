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
@description: Unittests for BOSWatch. File must be run as "pytest" unittest
"""

# import pytest  # import the pytest framework

from boswatch.descriptor import descriptor
from boswatch.packet import packet


class Test_Descriptor:
    """!Unittests for the descriptor"""

    def test_loadCSVnotExist(self):
        """!read CSV file where not exist direct per DescriptionList class"""
        descList = descriptor.DescriptionList()
        assert descList.loadCSV("boswatch") is False

    def test_loadCSV(self):
        """!read CSV file direct per DescriptionList class"""
        descList = descriptor.DescriptionList()
        assert descList.loadCSV("zvei") is True

    def test_descriptorLoadFailed(self):
        """!read CSV file where not exist"""
        bwDescriptor = descriptor.Descriptor()
        assert bwDescriptor.loadDescription("boswatch") is False

    def test_descriptorLoad(self):
        """!read CSV file"""
        bwDescriptor = descriptor.Descriptor()
        assert bwDescriptor.loadDescription("zvei") is True

    def test_loadDescriptionsNotSet(self):
        """!load descriptions where not set to an bwPacket"""
        bwDescriptor = descriptor.Descriptor()
        assert bwDescriptor.loadDescription("zvei") is True
        bwPacket = packet.Packet()
        bwPacket.setField("mode", "zvei")
        bwPacket.setField("zvei", "54321")
        assert bwDescriptor.addDescriptions(bwPacket) is True
        assert bwPacket.getField("shortDescription") is ""
        assert bwPacket.getField("longDescription") is ""

    def test_loadDescriptions(self):
        """!load descriptions to an bwPacket"""
        bwDescriptor = descriptor.Descriptor()
        assert bwDescriptor.loadDescription("zvei") is True
        bwPacket = packet.Packet()
        bwPacket.setField("mode", "zvei")
        bwPacket.setField("zvei", "12345")
        assert bwDescriptor.addDescriptions(bwPacket) is True
        assert bwPacket.getField("shortDescription") is not ""
        assert bwPacket.getField("longDescription") is not ""
