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
# problem of the pytest fixtures
# pylint: disable=redefined-outer-name
import logging
import time
import queue
import pytest

from boswatch.network.server import TCPServer
from boswatch.network.client import TCPClient
import threading


def setup_method(method):
    logging.debug("[TEST] %s.%s", method.__module__, method.__name__)


@pytest.fixture
def getClient():
    """!Build and serve a TCPCLient"""
    return TCPClient()


@pytest.fixture
def getServer():
    """!Build and serve a TCPServer"""
    dataQueue = queue.Queue()
    testServer = TCPServer(dataQueue)
    return testServer


@pytest.fixture
def getRunningServer(getServer):
    """!Build and serve a still running TCPServer"""
    logging.debug("start server")
    assert getServer.start()
    while not getServer.isRunning:
        pass
    yield getServer
    logging.debug("stop server")
    assert getServer.stop()
    time.sleep(0.1)  # wait for safe stopped


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


def test_doubleConnect(getClient, getRunningServer):
    """!Connect to a server twice"""
    assert getClient.connect()
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


@pytest.mark.skip("needs fixture for more than one client")
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
    assert getRunningServer._alarmQueue.qsize() == 3
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


def test_serverDoubleStart(getServer):
    """!Test to start the server twice"""
    assert getServer.start()
    assert getServer.start()
    assert getServer.stop()


def test_serverStartTwoInstances():
    """!Test to start two server different server instances"""
    dataQueue = queue.Queue()
    testServer1 = TCPServer(dataQueue)
    testServer2 = TCPServer(dataQueue)
    assert testServer1.start()
    assert testServer1.isRunning
    assert not testServer2.start()
    assert testServer1.isRunning
    assert not testServer2.isRunning
    assert testServer1.stop()
    assert testServer2.stop()


def test_serverStopsWhileConnected(getRunningServer, getClient):
    """!Shutdown server while client is connected"""
    getClient.connect()
    getRunningServer.stop()
    timeout = 5
    while getClient.isConnected:
        time.sleep(0.1)
        timeout = timeout - 1
        if timeout == 0:
            break
    assert timeout


@pytest.mark.skip("needs fixture for more than one client")
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
    assert getRunningServer._alarmQueue.qsize() == 2
    assert getRunningServer._alarmQueue.get(True, 1)[1] == "test1"
    assert getRunningServer._alarmQueue.get(True, 1)[1] == "test2"
    assert getRunningServer._alarmQueue.qsize() == 0  # Last _check must be None
    # disconnect all
    assert testClient1.disconnect()
    assert testClient2.disconnect()


def test_serverHighLoad(getRunningServer):
    """!High load server test with 10 send threads each will send 100 msg with 324 bytes size"""
    logging.debug("start sendThreads")
    threads = []
    for thr_id in range(10):
        thr = threading.Thread(target=sendThread, name="sendThread-" + str(thr_id))
        thr.daemon = True
        thr.start()
        threads.append(thr)
    for thread in threads:
        thread.join()
    logging.debug("finished sendThreads")
    assert getRunningServer._alarmQueue.qsize() == 1000


def sendThread():
    client = TCPClient()
    client.connect()
    time.sleep(0.1)
    for i in range(100):
        # actually this string is 324 bytes long
        client.transmit("HigLoadTestString-HigLoadTestString-HigLoadTestString-HigLoadTestString-HigLoadTestString-HigLoadTestString-"
                        "HigLoadTestString-HigLoadTestString-HigLoadTestString-HigLoadTestString-HigLoadTestString-HigLoadTestString-"
                        "HigLoadTestString-HigLoadTestString-HigLoadTestString-HigLoadTestString-HigLoadTestString-HigLoadTestString-")
        if not client.receive() == "[ack]":
            logging.error("missing [ACK]")

    time.sleep(0.1)
    client.disconnect()
