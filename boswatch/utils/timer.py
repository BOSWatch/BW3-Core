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

@file:        timer.py
@date:        21.09.2018
@author:      Bastian Schroll
@description: Timer class for interval timed events
"""
import logging
import time
from threading import Thread, Event

logging.debug("- %s loaded", __name__)


class RepeatedTimer:

    def __init__(self, interval, targetFunction, *args, **kwargs):
        """!Create a new instance of the RepeatedTimer

        @param interval: interval in sec. to recall target function
        @param targetFunction: function to call on timer event
        @param *args: arguments for the called function
        @param *kwargs: keyword arguments for the called function
        """
        self._interval = interval
        self._function = targetFunction
        self._args = args
        self._kwargs = kwargs
        self._start = 0
        self._event = Event()
        self._thread = None

    def start(self):
        """!Start a new timer worker thread"""
        self._event.clear()
        self._thread = Thread(target=self._target)
        self._thread.name = "RepTim(" + str(self._interval) + ")"
        self._start = time.time()
        self._thread.start()
        logging.debug("start repeatedTimer: %s", self._thread.name)

    def stop(self):
        """!Stop the timer worker thread"""
        self._event.set()
        self._thread.join()
        logging.debug("stop repeatedTimer: %s", self._thread.name)

    def _target(self):
        """!Runs the target function with his arguments"""
        while not self._event.wait(self.restTime):
            logging.debug("work")
            startTime = time.time()
            self._function(*self._args, **self._kwargs)
            time.sleep(1.5)
            runTime = time.time() - startTime

            if runTime < self._interval:
                logging.debug("ready after: %0.3f sec. - next call in: %0.3f sec.", runTime, self.restTime)
            else:
                logging.warning("timer overdue! interval: %0.3f sec. - runtime: %0.3f sec.", self._interval, runTime)

    @property
    def restTime(self):
        """!Property to get remaining time till next call"""
        return self._interval - ((time.time() - self._start) % self._interval)
