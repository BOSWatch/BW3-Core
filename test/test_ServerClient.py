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
import logging
import time
import queue
import pytest

from boswatch.network.server import TCPServer
from boswatch.network.client import TCPClient


class Test_ServerClient:
    """!Unittest for the server/client environment"""

    def setup_method(self, method):
        logging.debug("[TEST] %s.%s", type(self).__name__, method.__name__)

    @pytest.fixture(scope="function")
    def useServer(self):
        """!Start and serve the sever for each functions where useServer is given"""
        self.dataQueue = queue.Queue()
        self.testServer = TCPServer(self.dataQueue)
        logging.debug("start server")
        assert self.testServer.start()
        time.sleep(0.1)  # wait for server
        # serv the instances - created in self context
        yield 1
        try:
            logging.debug("stop server")
            self.testServer.stop()
        except:
            logging.warning("server still stopped")

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
        assert self.testServer.countClientsConnected() == 2
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
        assert self.dataQueue.qsize() == 3
        # disconnect all
        assert self.testClient1.disconnect()
        assert self.testClient2.disconnect()
        assert self.testClient3.disconnect()

    def test_serverRestart(self, useServer):
        """!Test a stop and restart of the server"""
        assert self.testServer.stop()
        assert self.testServer.start()
        assert self.testServer.stop()

    def test_serverStopFailed(self, useServer):
        """!Test to stop a stopped server"""
        assert self.testServer.stop()
        assert not self.testServer.stop()

    def test_serverDoubleStart(self):
        """!Test to start the server twice"""
        self.dataQueue = queue.Queue()
        self.testServer1 = TCPServer(self.dataQueue)
        self.testServer2 = TCPServer(self.dataQueue)
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
        assert self.testClient1.transmit("test1")
        time.sleep(0.1)  # wait for recv to prevent fail of false order
        assert self.testClient2.transmit("test2")
        # recv all
        assert self.testClient1.receive() == "[ack]"
        assert self.testClient2.receive() == "[ack]"
        # _check server output data
        assert self.dataQueue.qsize() == 2
        assert self.dataQueue.get(True, 1)[1] == "test1"
        assert self.dataQueue.get(True, 1)[1] == "test2"
        assert self.dataQueue.qsize() is 0  # Last _check must be None
        # disconnect all
        assert self.testClient1.disconnect()
        assert self.testClient2.disconnect()
