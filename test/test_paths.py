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
@description: Unittests for BOSWatch. File must be _run as "pytest" unittest
"""
import logging
import os

from boswatch.utils import paths


class Test_Config:
    """!Unittests for the paths"""

    def setup_method(self, method):
        logging.debug("[TEST] %s.%s", type(self).__name__, method.__name__)

    def test_fileExists(self):
        """!load a local config file"""
        assert paths.fileExist("README.md")

    def test_fileNotExists(self):
        """!load a local config file"""
        assert not paths.fileExist("notFound.txt")

    def test_makeDirNotExisting(self):
        """!load a local config file"""
        assert paths.makeDirIfNotExist("UnItTeSt")
        os.removedirs("UnItTeSt")

    def test_makeDirExisting(self):
        """!load a local config file"""
        paths.makeDirIfNotExist("UnItTeSt")
        assert paths.makeDirIfNotExist("UnItTeSt")
        os.removedirs("UnItTeSt")
