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
@description: Unittests for BOSWatch. File have to run as "pytest" unittest
"""
import logging
import pytest
from boswatch.utils import paths

from boswatch.configYaml import ConfigYAML


def setup_method(method):
    logging.debug("[TEST] %s.%s", method.__module__, method.__name__)


@pytest.fixture
def getConfig():
    return ConfigYAML()


@pytest.fixture
def getFilledConfig():
    filledConfig = ConfigYAML()
    assert filledConfig.loadConfigFile(paths.TEST_PATH + "test_config.yaml") is True
    return filledConfig


def test_loadConfigFile(getConfig):
    """!load a config file"""
    assert getConfig.loadConfigFile(paths.TEST_PATH + "test_config.yaml") is True


def test_loadConfigFileFailed(getConfig):
    """!load a config file with syntax error"""
    assert getConfig.loadConfigFile(paths.TEST_PATH + "test_configFailed.yaml") is False


def test_loadConfigFileNotFound(getConfig):
    """!load a config file where is not available"""
    assert getConfig.loadConfigFile(paths.TEST_PATH + "test_configNotFound.yaml") is False


def test_getTypes(getFilledConfig):
    assert type(getFilledConfig.get("types")) is ConfigYAML
    assert type(getFilledConfig.get("types", "string")) is str
    assert type(getFilledConfig.get("types", "bool")) is bool
    assert type(getFilledConfig.get("types", "integer")) is int
    assert type(getFilledConfig.get("types", "float")) is float


def test_getNestedConfig(getFilledConfig):
    nestedConfig = getFilledConfig.get("types")
    assert type(nestedConfig) is ConfigYAML
    assert nestedConfig.get("string") == "Hello World"


def test_configIterationList(getFilledConfig):
    counter = 0
    for item in getFilledConfig.get("list"):
        assert type(item) is str
        counter += 1
    assert counter == 3
