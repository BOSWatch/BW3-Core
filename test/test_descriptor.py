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


class Test_Descriptor:
    """!Unittests for the descriptor

    @todo Error because path's in paths.py are false when start over pytest"""

    def test_loadCSVnotExist(self):
        """!read CSV file where not exist"""
        descList = descriptor.DescriptionList("boswatch")
        assert bool(descList._getFullList()) is False

    def test_loadCSV(self):
        """!read CSV file"""
        descList = descriptor.DescriptionList("zvei")
        assert bool(descList._getFullList()) is True
