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

@file:        test_broadcast.py
@date:        25.09.2018
@author:      Bastian Schroll
@description: Unittests for BOSWatch. File have to run as "pytest" unittest
"""
# problem of the pytest fixtures
# pylint: disable=redefined-outer-name
import logging
import pytest

from boswatch.network.broadcast import BroadcastServer
from boswatch.network.broadcast import BroadcastClient


def setup_method(method):
    logging.debug("[TEST] %s.%s", method.__module__, method.__name__)


@pytest.fixture()
def broadcastServer():
    """!Server a BroadcastServer instance"""
    broadcastServer = BroadcastServer()
    yield broadcastServer
    if broadcastServer.isRunning:
        assert broadcastServer.stop()
    while broadcastServer.isRunning:
        pass


@pytest.fixture()
def broadcastClient():
    """!Server a BroadcastClient instance"""
    return BroadcastClient()


def test_serverStartStop(broadcastServer):
    """!Start a BroadcastServer, check if running and stop it"""
    assert broadcastServer.start()
    assert broadcastServer.isRunning
    assert broadcastServer.stop()


def test_serverDoubleStart(broadcastServer):
    """!Try to start a BroadcastServer twice"""
    assert broadcastServer.start()
    assert broadcastServer.start()
    assert broadcastServer.stop()


def test_serverStopNotStarted(broadcastServer):
    """!Try to stop a BroadcastServer where is not running"""
    assert broadcastServer.stop()


def test_clientWithoutServer(broadcastClient):
    """!Use BroadcastClient with no server"""
    assert not broadcastClient.getConnInfo(1)


def test_serverClientFetchConnInfo(broadcastClient, broadcastServer):
    """!Fetch connection info from BroadcastServer"""
    assert broadcastServer.start()
    assert broadcastClient.getConnInfo()
    assert broadcastServer.stop()
    assert broadcastClient.serverIP
    assert broadcastClient.serverPort
