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

@file:        test_doubleFilter.py
@date:        15.12.2017
@author:      Bastian Schroll
@description: Unittests for BOSWatch. File must be _run as "pytest" unittest
"""
import logging

from module.filter.doubleFilter import DoubleFilter


class Test_DoubleFilter:

    def setup_method(self, method):
        logging.debug("[TEST] %s.%s", type(self).__name__, method.__name__)

    def test_none(self):
        pass
