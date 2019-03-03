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

@file:        test_ServerClient.py
@date:        10.12.2017
@author:      Bastian Schroll
@description: Unittests for BOSWatch. File have to run as "pytest" unittest
"""
import logging
import time
import queue
import pytest

from boswatch.network.server import TCPServer
from boswatch.network.client import TCPClient


def setup_method(method):
    logging.debug("[TEST] %s.%s", method.__module__, method.__name__)


@pytest.fixture
def getClient():
    return TCPClient()


@pytest.fixture
def getServer():
    """!Start and serve the sever for each functions where useServer is given"""
    dataQueue = queue.Queue()
    testServer = TCPServer(dataQueue)
    return testServer


@pytest.fixture
def getRunningServer(getServer):
    logging.debug("start server")
    assert getServer.start()
    if not getServer.isRunning:
        pytest.fail("server not running")
    yield getServer
    logging.debug("stop server")
    assert getServer.stop()


def test_clientConnectFailed(getClient):
    """!Connect to a non available server"""
    assert not getClient.connect()


def test_clientDisconnectFailed(getClient):
    """!Disconnect while no connection is established"""
    assert getClient.disconnect()


def test_clientTransmitFailed(getClient):
    """!Transmit while no connection is established"""
    assert not getClient.transmit("test")


def test_clientReceiveFailed(getClient):
    """!Receive while no connection is established"""
    assert not getClient.receive()


def test_clientConnect(getClient, getRunningServer):
    """!Connect to a server"""
    assert getClient.connect()
    assert getClient.disconnect()


def test_clientReconnect(getClient, getRunningServer):
    """!Try a reconnect after a established connection"""
    assert getClient.connect()
    assert getClient.disconnect()
    assert getClient.connect()
    assert getClient.disconnect()


def test_clientMultiConnect(getClient, getRunningServer):
    """!Connect with 2 clients to the server"""
    assert getClient.connect()
    testClient2 = TCPClient()
    assert testClient2.connect()
    time.sleep(0.1)  # wait for all clients connected
    # check connected clients
    assert getRunningServer.countClientsConnected() == 2
    # disconnect all
    assert getClient.disconnect()
    assert testClient2.disconnect()


def test_clientCommunicate(getClient, getRunningServer):
    """!Try to send data to the server and check on '[ack]'"""
    assert getClient.connect()
    assert getClient.transmit("test")
    assert getClient.receive() == "[ack]"
    assert getClient.disconnect()


def test_clientMultiCommunicate(getServer):
    """!Try to send data to the server with 3 clients and check on '[ack]'"""
    # connect all
    testClient1 = TCPClient()
    assert testClient1.connect()
    testClient2 = TCPClient()
    assert testClient2.connect()
    testClient3 = TCPClient()
    assert testClient3.connect()
    # send all
    assert testClient1.transmit("test")
    assert testClient2.transmit("test")
    assert testClient3.transmit("test")
    # recv all
    assert testClient3.receive() == "[ack]"
    assert testClient2.receive() == "[ack]"
    assert testClient1.receive() == "[ack]"
    # check server msg queue
    assert dataQueue.qsize() == 3
    # disconnect all
    assert testClient1.disconnect()
    assert testClient2.disconnect()
    assert testClient3.disconnect()


def test_serverRestart(getRunningServer):
    """!Test a stop and restart of the server"""
    assert getRunningServer.stop()
    assert getRunningServer.start()
    assert getRunningServer.stop()


def test_serverStopFailed(getServer):
    """!Test to stop a stopped server"""
    assert getServer.stop()


def test_serverDoubleStart():
    """!Test to start the server twice"""
    dataQueue = queue.Queue()
    testServer1 = TCPServer(dataQueue)
    testServer2 = TCPServer(dataQueue)
    assert testServer1.start()
    assert not testServer2.start()
    assert testServer1.stop()
    assert testServer2.stop()


def test_serverGetOutput(getRunningServer):
    """!Send data to server with 2 clients, check '[ack]' and data on server queue"""
    # connect all
    testClient1 = TCPClient()
    assert testClient1.connect()
    testClient2 = TCPClient()
    assert testClient2.connect()
    # send all
    assert testClient1.transmit("test1")
    time.sleep(0.1)  # wait for recv to prevent fail of false order
    assert testClient2.transmit("test2")
    # recv all
    assert testClient1.receive() == "[ack]"
    assert testClient2.receive() == "[ack]"
    # _check server output data
    assert dataQueue.qsize() == 2
    assert dataQueue.get(True, 1)[1] == "test1"
    assert dataQueue.get(True, 1)[1] == "test2"
    assert dataQueue.qsize() is 0  # Last _check must be None
    # disconnect all
    assert testClient1.disconnect()
    assert testClient2.disconnect()
