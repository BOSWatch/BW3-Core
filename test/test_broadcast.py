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
@description: Unittests for BOSWatch. File must be _run as "pytest" unittest
"""
import logging
import time
import pytest

from boswatch.network.broadcast import BroadcastServer
from boswatch.network.broadcast import BroadcastClient


class Test_Broadcast:
    """!Unittest for the timer class"""

    def setup_method(self, method):
        logging.debug("[TEST] %s.%s", type(self).__name__, method.__name__)

    @pytest.fixture(scope="function")
    def useBroadcastServer(self):
        """!Server a BroadcastServer instance"""
        self.broadcastServer = BroadcastServer()
        yield 1  # server the server instance
        if self.broadcastServer.isRunning:
            assert self.broadcastServer.stop()
        while self.broadcastServer.isRunning:
            pass

    @pytest.fixture(scope="function")
    def useBroadcastClient(self):
        """!Server a BroadcastClient instance"""
        self.broadcastClient = BroadcastClient()
        yield 1  # server the server instance

    # tests start here

    def test_serverStartStop(self, useBroadcastServer):
        assert self.broadcastServer.start()
        assert self.broadcastServer.isRunning
        assert self.broadcastServer.stop()

    def test_serverDoubleStart(self, useBroadcastServer):
        assert self.broadcastServer.start()
        assert self.broadcastServer.start()
        assert self.broadcastServer.stop()

    def test_serverStopNotStarted(self, useBroadcastServer):
        assert self.broadcastServer.stop()

    def test_clientWithoutServer(self, useBroadcastClient):
        assert not self.broadcastClient.getConnInfo(1)

    def test_serverClientFetchConnInfo(self, useBroadcastServer, useBroadcastClient):
        assert self.broadcastServer.start()
        assert self.broadcastClient.getConnInfo()
        assert self.broadcastServer.stop()
        assert self.broadcastClient.serverIP
        assert self.broadcastClient.serverPort
