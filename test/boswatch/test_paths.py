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

@file:        test_paths.py
@date:        22.02.2017
@author:      Bastian Schroll
@description: Unittests for BOSWatch. File have to run as "pytest" unittest
"""
import logging
import os

from boswatch.utils import paths


def setup_method(method):
    logging.debug("[TEST] %s.%s", method.__module__, method.__name__)


def test_fileExists():
    """!load a local config file"""
    assert paths.fileExist("README.md")


def test_fileNotExists():
    """!load a local config file"""
    assert not paths.fileExist("notFound.txt")


def test_makeDirNotExisting():
    """!load a local config file"""
    assert paths.makeDirIfNotExist("UnItTeSt")
    os.removedirs("UnItTeSt")


def test_makeDirExisting():
    """!load a local config file"""
    paths.makeDirIfNotExist("UnItTeSt")
    assert paths.makeDirIfNotExist("UnItTeSt")
    os.removedirs("UnItTeSt")
