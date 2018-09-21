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

@file:        test_timer.py
@date:        21.09.2019
@author:      Bastian Schroll
@description: Unittests for BOSWatch. File must be _run as "pytest" unittest
"""
import logging
import time
import pytest

from boswatch.utils.timer import RepeatedTimer


class Test_Timer:
    """!Unittest for the timer class"""

    def setup_method(self, method):
        logging.debug("[TEST] %s.%s", type(self).__name__, method.__name__)

    @staticmethod
    def testTarget():
        logging.debug("run testTarget")

    @pytest.fixture(scope="function")
    def useTimer(self):
        """!Server a RepeatedTimer instance"""
        self.testTimer = RepeatedTimer(0.5, Test_Timer.testTarget)
        time.sleep(0.1)
        yield 1

    def test_timerStartStop(self, useTimer):
        assert self.testTimer.start()
        assert self.testTimer.stop()

    def test_timerStopNotStarted(self, useTimer):
        assert not self.testTimer.stop()

    def test_timerRun(self, useTimer):
        assert self.testTimer.start()
        time.sleep(0.6)
        assert self.testTimer.stop()
