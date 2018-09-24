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
@date:        21.09.2018
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
    def testTargetFast():
        """!Fast worker thread"""
        logging.debug("run testTargetFast")

    @staticmethod
    def testTargetSlow():
        """!Slow worker thread"""
        logging.debug("run testTargetSlow start")
        time.sleep(0.51)
        logging.debug("run testTargetSlow end")

    @pytest.fixture(scope="function")
    def useTimerFast(self):
        """!Server a RepeatedTimer instance with fast worker"""
        self.testTimer = RepeatedTimer(0.1, Test_Timer.testTargetFast)
        yield 1  # server the timer instance
        if self.testTimer.isRunning:
            self.testTimer.stop()

    @pytest.fixture(scope="function")
    def useTimerSlow(self):
        """!Server a RepeatedTimer instance slow worker"""
        self.testTimer = RepeatedTimer(0.1, Test_Timer.testTargetSlow)
        yield 1  # server the timer instance
        if self.testTimer.isRunning:
            self.testTimer.stop()

    # test cases starts here

    def test_timerStartStop(self, useTimerFast):
        assert self.testTimer.start()
        assert self.testTimer.stop()

    def test_timerDoubleSTart(self, useTimerFast):
        assert self.testTimer.start()
        assert self.testTimer.start()
        assert self.testTimer.stop()

    def test_timerStopNotStarted(self, useTimerFast):
        assert not self.testTimer.stop()

    def test_timerIsRunning(self, useTimerFast):
        assert self.testTimer.start()
        assert self.testTimer.isRunning
        assert self.testTimer.stop()

    def test_timerRun(self, useTimerFast):
        assert self.testTimer.start()
        time.sleep(0.2)
        assert self.testTimer.stop()
        assert self.testTimer.overdueCount == 0
        assert self.testTimer.lostEvents == 0

    def test_timerOverdue(self, useTimerSlow):
        assert self.testTimer.start()
        time.sleep(0.2)
        assert self.testTimer.stop()
        assert self.testTimer.overdueCount == 1
        assert self.testTimer.lostEvents == 5

    def test_timerOverdueLong(self, useTimerSlow):
        assert self.testTimer.start()
        time.sleep(1)
        assert self.testTimer.stop()
        assert self.testTimer.overdueCount == 2
        assert self.testTimer.lostEvents == 10
