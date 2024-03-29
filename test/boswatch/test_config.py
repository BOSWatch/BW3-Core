#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""!
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
# problem of the pytest fixtures
# pylint: disable=redefined-outer-name
import logging
import pytest
from boswatch.utils import paths

from boswatch.configYaml import ConfigYAML


def setup_function(function):
    logging.debug("[TEST] %s.%s", function.__module__, function.__name__)


@pytest.fixture
def getConfig():
    r"""!Build a config object"""
    return ConfigYAML()


@pytest.fixture
def getFilledConfig():
    r"""!Build a config object and fill it with the config data"""
    filledConfig = ConfigYAML()
    assert filledConfig.loadConfigFile(paths.TEST_PATH + "test_config.yaml") is True
    return filledConfig


def test_loadConfigFile(getConfig):
    r"""!load a config file"""
    assert getConfig.loadConfigFile(paths.TEST_PATH + "test_config.yaml") is True


def test_loadConfigFileFailed(getConfig):
    r"""!load a config file with syntax error"""
    assert getConfig.loadConfigFile(paths.TEST_PATH + "test_configFailed.yaml") is False


def test_loadConfigFileNotFound(getConfig):
    r"""!load a config file where is not available"""
    assert getConfig.loadConfigFile(paths.TEST_PATH + "test_configNotFound.yaml") is False


def test_getConfigAsString(getFilledConfig):
    r"""!Get the string representation of the config"""
    assert type(str(getFilledConfig)) is str
    logging.debug(getFilledConfig)


def test_getTypes(getFilledConfig):
    r"""!Get and check different data types in config"""
    assert type(getFilledConfig.get("types")) is ConfigYAML
    assert type(getFilledConfig.get("types", "string")) is str
    assert type(getFilledConfig.get("types", "bool")) is bool
    assert type(getFilledConfig.get("types", "integer")) is int
    assert type(getFilledConfig.get("types", "float")) is float


def test_getDefaultValue(getFilledConfig):
    r"""!Get the default value of an not existent entry"""
    assert getFilledConfig.get("notExistent", default="defaultValue") == "defaultValue"


def test_getNestedConfig(getFilledConfig):
    r"""!Work with nested sub-config elements"""
    nestedConfig = getFilledConfig.get("types")
    assert type(nestedConfig) is ConfigYAML
    assert nestedConfig.get("string") == "Hello World"


def test_configIterationList(getFilledConfig):
    r"""!Try to iterate over a list in the config"""
    counter = 0
    for item in getFilledConfig.get("list"):
        assert type(item) is str
        counter += 1
    assert counter == 3


def test_configIterationListWithNestedList(getFilledConfig):
    r"""!Try to iterate over a list in the config where its elements are lists itself"""
    listCnt = 0
    strCnt = 0
    for item in getFilledConfig.get("list1"):
        if type(item) is ConfigYAML:
            listCnt += 1
        if type(item) is str:
            strCnt += 1
    assert listCnt == 2
    assert strCnt == 1
