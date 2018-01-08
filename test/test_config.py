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

@file:        test_config.py
@date:        08.01.2017
@author:      Bastian Schroll
@description: Unittests for BOSWatch. File must be run as "pytest" unittest
"""

# import pytest  # import the pytest framework

from boswatch.utils import paths
from boswatch.config import Config


class Test_Config:
    """!Unittests for the config"""

    def test_loadLocalConfig(self):
        """!load a local config file"""
        bwConfig = Config(paths.TEST_PATH + "test.ini")
        assert bwConfig._config is not None

    def test_getLocalConfig(self):
        """!get values from local config file"""
        bwConfig = Config(paths.TEST_PATH + "test.ini")
        assert bwConfig.getConfig("test", "one") == "1"
        assert bwConfig.getConfig("test", "two") == "two"
        assert bwConfig.getConfig("testcase", "test") == "ok"

    def test_getLocalConfigFailed(self):
        """!fail while get values from local config file"""
        bwConfig = Config(paths.TEST_PATH + "test.ini")
        assert bwConfig.getConfig("test", "abc") is None
        assert bwConfig.getConfig("abc", "test") is None

    def test_shareConfig(self):
        """!load local config file and share it"""
        bwConfig = Config(paths.TEST_PATH + "test.ini", "test_shareConfig")
        assert bwConfig._sharedConfig["test_shareConfig"] is not None

    def test_shareConfigUsed(self):
        """!load local config file and tr to share it twice with same name"""
        bwConfig1 = Config(paths.TEST_PATH + "test.ini", "test_shareConfigUsed")
        assert bwConfig1._sharedConfig["test_shareConfigUsed"] is not None
        bwConfig2 = Config(paths.TEST_PATH + "test.ini")
        assert bwConfig2._shareConfig("test_shareConfigUsed") is False

    def test_getNotSetSharedConfig(self):
        """!try to get values from shared config where not exists"""
        bwConfig = Config(paths.TEST_PATH + "test.ini")
        assert bwConfig.getConfig("test", "one") == "1"
        assert bwConfig.getConfig("test", "one", "NotSetSharedConfig") is None

    def test_getSharedConfig(self):
        """!get values from shared config file"""
        bwConfig1 = Config(paths.TEST_PATH + "test.ini", "test_getSharedConfig")
        assert bwConfig1._sharedConfig["test_getSharedConfig"] is not None

        bwConfig2 = Config()
        assert bwConfig2.getConfig("test", "one") is None
        assert bwConfig2.getConfig("test", "one", "test_getSharedConfig") == "1"

    def test_getSharedConfigFailed(self):
        """!fail while get values from shared config file"""
        bwConfig1 = Config(paths.TEST_PATH + "test.ini", "test_getSharedConfigFailed")
        assert bwConfig1._sharedConfig["test_getSharedConfigFailed"] is not None

        bwConfig2 = Config()
        assert bwConfig2.getConfig("test", "abc", "test_getSharedConfigFailed") is None
        assert bwConfig2.getConfig("abc", "test", "test_getSharedConfigFailed") is None
