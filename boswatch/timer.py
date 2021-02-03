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
        self.overdueCount = 0
        self.lostEvents = 0
        self._isRunning = False
        self._event = Event()
        self._thread = None

    def start(self):
        """!Start a new timer worker thread

        @return True or False"""
        if self._thread is None:
            self._event.clear()
            self._thread = Thread(target=self._target)
            self._thread.name = "RepTim(" + str(self._interval) + ")"
            self._thread.daemon = True  # start as daemon (thread dies if main program ends)
            self._thread.start()
            logging.debug("start repeatedTimer: %s", self._thread.name)
            return True
        logging.debug("repeatedTimer always started")
        return True

    def stop(self):
        """!Stop the timer worker thread

        @return True or False"""
        if self._thread is not None:
            logging.debug("stop repeatedTimer: %s", self._thread.name)
            self._event.set()
            self._thread.join()
            return True
        logging.warning("repeatedTimer always stopped")
        return True

    def _target(self):
        """!Runs the target function with his arguments in own thread"""
        self._start = time.time()
        while not self._event.wait(self.restTime):
            logging.debug("work")
            startTime = time.time()

            try:
                self._function(*self._args, **self._kwargs)
            except:  # pragma: no cover
                logging.exception("target throws an exception")

            runTime = time.time() - startTime
            if runTime < self._interval:
                logging.debug("ready after: %0.3f sec. - next call in: %0.3f sec.", runTime, self.restTime)
            else:
                lostEvents = int(runTime / self._interval)
                logging.warning("timer overdue! interval: %0.3f sec. - runtime: %0.3f sec. - "
                                "%d events lost - next call in: %0.3f sec.", self._interval, runTime, lostEvents, self.restTime)
                self.lostEvents += lostEvents
                self.overdueCount += 1
        logging.debug("repeatedTimer thread stopped: %s", self._thread.name)
        self._thread = None  # set to none after leave teh thread (running recognize)

    @property
    def isRunning(self):
        """!Property for repeatedTimer running state"""
        if self._thread:
            return True
        return False

    @property
    def restTime(self):
        """!Property to get remaining time till next call"""
        return self._interval - ((time.time() - self._start) % self._interval)
