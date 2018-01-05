#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    ____  ____  ______       __      __       __       _____
   / __ )/ __ \/ ___/ |     / /___ _/ /______/ /_     |__  /
  / __  / / / /\__ \| | /| / / __ `/ __/ ___/ __ \     /_ <
 / /_/ / /_/ /___/ /| |/ |/ / /_/ / /_/ /__/ / / /   ___/ /
/_____/\____//____/ |__/|__/\__,_/\__/\___/_/ /_/   /____/
                German BOS Information Script
                     by Bastian Schroll

@file:        test_header.py
@date:        12.12.2017
@author:      Bastian Schroll
@description: Unittests for BOSWatch. File must be run as "pytest" unittest
"""


# import pytest  # import the pytest framework

import boswatch.utils.header


class Test_Header:
    """!Unittests for the header"""

    def test_logoToLog(self):
        """!Test logo to log"""
        assert boswatch.utils.header.logoToLog()

    def test_infoToLog(self):
        """!Test info to log"""
        assert boswatch.utils.header.infoToLog()

    def test_logoToScreen(self):
        """!Test logo to screen"""
        assert boswatch.utils.header.logoToScreen()
