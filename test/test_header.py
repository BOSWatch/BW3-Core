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

@file:        test_header.py
@date:        12.12.2017
@author:      Bastian Schroll
@description: Unittests for BOSWatch. File must be _run as "pytest" unittest
"""
import logging

from boswatch.utils import header


class Test_Header:
    """!Unittests for the header"""

    def setup_method(self, method):
        logging.debug("[TEST] %s.%s", type(self).__name__, method.__name__)

    def test_logoToLog(self):
        """!Test logo to log"""
        assert header.logoToLog()

    def test_infoToLog(self):
        """!Test info to log"""
        assert header.infoToLog()

    def test_logoToScreen(self):
        """!Test logo to screen"""
        assert header.logoToScreen()
