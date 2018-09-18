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
@description: Unittests for BOSWatch. File must be _run as "pytest" unittest
"""
import pytest
import logging
import time

from boswatch.network.server import TCPServer
from boswatch.network.client import TCPClient


class Test_ServerClient:
    """!Unittest for the server/client environment"""

    def setup_method(self, method):
        logging.debug("[TEST] %s.%s", (type(self).__name__, method.__name__))

    @pytest.fixture(scope="function")
    def useServer(self):
        """!Start and serve the sever for each functions where useServer is given"""
        self.testServer = TCPServer()
        assert self.testServer.start()
        time.sleep(0.1)  # wait for server
        yield self.testServer  # server to all test where useServer is given
        assert self.testServer.stop()
        time.sleep(0.1)  # wait for server

    def test_clientConnectFailed(self):
        """!Connect to a non available server"""
        self.testClient = TCPClient()
        assert not self.testClient.connect()

    def test_clientDisconnectFailed(self):
        """!Disconnect while no connection is established"""
        self.testClient = TCPClient()
        assert not self.testClient.disconnect()

    def test_clientTransmitFailed(self):
        """!Transmit while no connection is established"""
        self.testClient = TCPClient()
        assert not self.testClient.transmit("test")

    def test_clientReceiveFailed(self):
        """!Receive while no connection is established"""
        self.testClient = TCPClient()
        assert not self.testClient.receive()

    def test_clientConnect(self, useServer):
        """!Connect to a server"""
        self.testClient = TCPClient()
        assert self.testClient.connect()
        assert self.testClient.disconnect()

    def test_clientReconnect(self, useServer):
        """!Try a reconnect after a established connection"""
        self.testClient = TCPClient()
        assert self.testClient.connect()
        assert self.testClient.disconnect()
        assert self.testClient.connect()
        assert self.testClient.disconnect()

    def test_clientMultiConnect(self, useServer):
        """!Connect with 2 clients to the server"""
        self.testClient1 = TCPClient()
        assert self.testClient1.connect()
        self.testClient2 = TCPClient()
        assert self.testClient2.connect()
        time.sleep(0.1)  # wait for all clients connected
        # check connected clients
        assert useServer.countClientsConnected() == 2
        # disconnect all
        assert self.testClient1.disconnect()
        assert self.testClient2.disconnect()

    def test_clientCommunicate(self, useServer):
        """!Try to send data to the server and check on '[ack]'"""
        self.testClient = TCPClient()
        assert self.testClient.connect()
        assert self.testClient.transmit("test")
        assert self.testClient.receive() == "[ack]"
        assert self.testClient.disconnect()

    def test_clientMultiCommunicate(self, useServer):
        """!Try to send data to the server with 3 clients and check on '[ack]'"""
        # connect all
        self.testClient1 = TCPClient()
        assert self.testClient1.connect()
        self.testClient2 = TCPClient()
        assert self.testClient2.connect()
        self.testClient3 = TCPClient()
        assert self.testClient3.connect()
        # send all
        assert self.testClient1.transmit("test")
        assert self.testClient2.transmit("test")
        assert self.testClient3.transmit("test")
        # recv all
        assert self.testClient3.receive() == "[ack]"
        assert self.testClient2.receive() == "[ack]"
        assert self.testClient1.receive() == "[ack]"
        # check server msg queue
        assert useServer.countPacketsInQueue() == 3
        # disconnect all
        assert self.testClient1.disconnect()
        assert self.testClient2.disconnect()
        assert self.testClient3.disconnect()

    def test_serverRestart(self):
        """!Test a restart of the server"""
        self.testServer = TCPServer()
        assert self.testServer.start()
        assert self.testServer.stop()
        assert self.testServer.start()
        assert self.testServer.stop()

    def test_serverStopFailed(self):
        """!Test to start the server twice"""
        self.testServer = TCPServer()
        assert not self.testServer.stop()

    def test_serverDoubleStart(self):
        """!Test to start the server twice"""
        self.testServer1 = TCPServer()
        self.testServer2 = TCPServer()
        assert self.testServer1.start()
        assert not self.testServer2.start()
        assert self.testServer1.stop()
        assert not self.testServer2.stop()

    def test_serverGetOutput(self, useServer):
        """!Send data to server with 2 clients, check '[ack]' and data on server queue"""
        # connect all
        self.testClient1 = TCPClient()
        assert self.testClient1.connect()
        self.testClient2 = TCPClient()
        assert self.testClient2.connect()
        # send all
        useServer.flushQueue()
        assert self.testClient1.transmit("test1")
        time.sleep(0.1)  # wait for recv to prevent fail of false order
        assert self.testClient2.transmit("test2")
        # recv all
        assert self.testClient1.receive() == "[ack]"
        assert self.testClient2.receive() == "[ack]"
        # _check server output data
        assert useServer.countPacketsInQueue() == 2
        assert useServer.getDataFromQueue()[1] == "test1"
        assert useServer.getDataFromQueue()[1] == "test2"
        assert useServer.getDataFromQueue() is None  # Last _check must be None
        # disconnect all
        assert self.testClient1.disconnect()
        assert self.testClient2.disconnect()
