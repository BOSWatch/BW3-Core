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
@description: Unittests for BOSWatch. File have to run as "pytest" unittest
"""
import logging

from boswatch.utils import header


def setup_method(method):
    logging.debug("[TEST] %s.%s", method.__module__, method.__name__)


def test_logoToLog():
    """!Test logo to log"""
    assert header.logoToLog()


def test_infoToLog():
    """!Test info to log"""
    assert header.infoToLog()
