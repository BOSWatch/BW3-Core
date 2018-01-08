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

import pytest  # import the pytest framework
import time

import boswatch.network.server
import boswatch.network.client


class Test_ServerClient:
    """!Unittest for the server/client environment"""

    @pytest.fixture(scope="function")
    def useServer(self):
        """!Start and serve the sever for each functions where useServer is given"""
        self.testServer = boswatch.network.server.TCPServer()
        assert self.testServer.start()
        time.sleep(0.1)  # wait for server
        yield self.testServer  # server to all test where useServer is given
        assert self.testServer.stop()
        time.sleep(0.1)  # wait for server

    def test_client_failed_connect(self):
        """!Connect to a non available server"""
        self.testClient = boswatch.network.client.TCPClient()
        assert not self.testClient.connect()

    def test_client_failed_disconnect(self):
        """!Disconnect while no connection is established"""
        self.testClient = boswatch.network.client.TCPClient()
        assert not self.testClient.disconnect()

    def test_client_failed_transmit(self):
        """!Transmit while no connection is established"""
        self.testClient = boswatch.network.client.TCPClient()
        assert not self.testClient.transmit("test")

    def test_client_failed_receive(self):
        """!Receive while no connection is established"""
        self.testClient = boswatch.network.client.TCPClient()
        assert not self.testClient.receive()

    def test_client_success_connect(self, useServer):
        """!Connect to a server"""
        self.testClient = boswatch.network.client.TCPClient()
        assert self.testClient.connect()
        assert self.testClient.disconnect()

    def test_client_reconnect(self, useServer):
        """!Try a reconnect after a established connection"""
        self.testClient = boswatch.network.client.TCPClient()
        assert self.testClient.connect()
        assert self.testClient.disconnect()
        assert self.testClient.connect()
        assert self.testClient.disconnect()

    def test_multi_connect(self, useServer):
        """!Connect with 2 clients to the server"""
        self.testClient1 = boswatch.network.client.TCPClient()
        assert self.testClient1.connect()
        self.testClient2 = boswatch.network.client.TCPClient()
        assert self.testClient2.connect()
        # disconnect all
        assert self.testClient1.disconnect()
        assert self.testClient2.disconnect()

    def test_client_communicate(self, useServer):
        """!Try to send data to the server and check on '[ack]'"""
        self.testClient = boswatch.network.client.TCPClient()
        assert self.testClient.connect()
        assert self.testClient.transmit("test")
        assert self.testClient.receive() == "[ack]"
        assert self.testClient.disconnect()

    def test_client_multi_communicate(self, useServer):
        """!Try to send data to the server with 3 clients and check on '[ack]'"""
        # connect all
        self.testClient1 = boswatch.network.client.TCPClient()
        assert self.testClient1.connect()
        self.testClient2 = boswatch.network.client.TCPClient()
        assert self.testClient2.connect()
        self.testClient3 = boswatch.network.client.TCPClient()
        assert self.testClient3.connect()
        # send all
        assert self.testClient1.transmit("test")
        assert self.testClient2.transmit("test")
        assert self.testClient3.transmit("test")
        # recv all
        assert self.testClient3.receive() == "[ack]"
        assert self.testClient2.receive() == "[ack]"
        assert self.testClient1.receive() == "[ack]"
        # disconnect all
        assert self.testClient1.disconnect()
        assert self.testClient2.disconnect()
        assert self.testClient3.disconnect()

    def test_server_restart(self):
        """!Test a restart of the server"""
        self.testServer = boswatch.network.server.TCPServer()
        assert self.testServer.start()
        assert self.testServer.stop()
        assert self.testServer.start()
        assert self.testServer.stop()

    def test_server_failed_stop(self):
        """!Test to start the server twice"""
        self.testServer = boswatch.network.server.TCPServer()
        assert not self.testServer.stop()

    def test_server_doubleStart(self):
        """!Test to start the server twice"""
        self.testServer1 = boswatch.network.server.TCPServer()
        self.testServer2 = boswatch.network.server.TCPServer()
        assert self.testServer1.start()
        assert not self.testServer2.start()
        assert self.testServer1.stop()
        assert not self.testServer2.stop()

    def test_server_output(self, useServer):
        """!Send data to server with 2 clients, check '[ack]' and data on server queue"""
        # connect all
        self.testClient1 = boswatch.network.client.TCPClient()
        assert self.testClient1.connect()
        self.testClient2 = boswatch.network.client.TCPClient()
        assert self.testClient2.connect()
        # send all
        useServer.flushData()
        assert self.testClient1.transmit("test1")
        time.sleep(0.1)  # wait for recv to prevent fail of false order
        assert self.testClient2.transmit("test2")
        # recv all
        assert self.testClient1.receive() == "[ack]"
        assert self.testClient2.receive() == "[ack]"
        # check server output data
        assert useServer.getData() == ("127.0.0.1", "test1")
        assert useServer.getData() == ("127.0.0.1", "test2")
        assert useServer.getData() is None  # Last check must be None
        # disconnect all
        assert self.testClient1.disconnect()
        assert self.testClient2.disconnect()
