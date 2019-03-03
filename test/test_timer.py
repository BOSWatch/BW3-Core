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
@description: Unittests for BOSWatch. File have to run as "pytest" unittest
"""
import logging
import time
import pytest

from boswatch.utils.timer import RepeatedTimer


def setup_method(method):
    logging.debug("[TEST] %s.%s", method.__module__, method.__name__)


def testTargetFast():
    """!Fast worker thread"""
    logging.debug("run testTargetFast")


def testTargetSlow():
    """!Slow worker thread"""
    logging.debug("run testTargetSlow start")
    time.sleep(0.51)
    logging.debug("run testTargetSlow end")


@pytest.fixture()
def useTimerFast():
    """!Server a RepeatedTimer instance with fast worker"""
    testTimer = RepeatedTimer(0.1, testTargetFast)
    yield testTimer
    if testTimer.isRunning:
        assert testTimer.stop()


@pytest.fixture()
def useTimerSlow():
    """!Server a RepeatedTimer instance slow worker"""
    testTimer = RepeatedTimer(0.1, testTargetSlow)
    yield testTimer
    if testTimer.isRunning:
        assert testTimer.stop()


def test_timerStartStop(useTimerFast):
    assert useTimerFast.start()
    assert useTimerFast.stop()


def test_timerDoubleStart(useTimerFast):
    assert useTimerFast.start()
    assert useTimerFast.start()
    assert useTimerFast.stop()


def test_timerStopNotStarted(useTimerFast):
    assert useTimerFast.stop()


def test_timerIsRunning(useTimerFast):
    assert useTimerFast.start()
    assert useTimerFast.isRunning
    assert useTimerFast.stop()


def test_timerRun(useTimerFast):
    assert useTimerFast.start()
    time.sleep(0.2)
    assert useTimerFast.stop()
    assert useTimerFast.overdueCount == 0
    assert useTimerFast.lostEvents == 0


def test_timerOverdue(useTimerSlow):
    assert useTimerSlow.start()
    time.sleep(0.2)
    assert useTimerSlow.stop()
    assert useTimerSlow.overdueCount == 1
    assert useTimerSlow.lostEvents == 5


def test_timerOverdueLong(useTimerSlow):
    assert useTimerSlow.start()
    time.sleep(1)
    assert useTimerSlow.stop()
    assert useTimerSlow.overdueCount == 2
    assert useTimerSlow.lostEvents == 10
