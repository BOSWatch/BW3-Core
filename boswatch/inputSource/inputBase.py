#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""!
    ____  ____  ______       __      __       __       _____
   / __ )/ __ \/ ___/ |     / /___ _/ /______/ /_     |__  /
  / __  / / / /\__ \| | /| / / __ `/ __/ ___/ __ \     /_ <
 / /_/ / /_/ /___/ /| |/ |/ / /_/ / /_/ /__/ / / /   ___/ /
/_____/\____//____/ |__/|__/\__,_/\__/\___/_/ /_/   /____/
                German BOS Information Script
                     by Bastian Schroll

@file:        inoutSource.py
@date:        28.10.2018
@author:      Bastian Schroll
@description: Base class for boswatch input sources
"""
import time
import logging
import threading
from abc import ABC, abstractmethod
from boswatch.utils import paths
from boswatch.processManager import ProcessManager
from boswatch.decoder.decoder import Decoder

logging.debug("- %s loaded", __name__)


class InputBase(ABC):
    r"""!Base class for handling inout sources"""

    def __init__(self, inputQueue, inputConfig, decoderConfig):
        r"""!Build a new InputSource class

        @param  inputQueue: Python queue object to store input data
        @param inputConfig: ConfigYaml object with the inoutSource config
        @param decoderConfig: ConfigYaml object with the decoder config"""
        self._inputThread = None
        self._isRunning = False
        self._inputQueue = inputQueue
        self._inputConfig = inputConfig
        self._decoderConfig = decoderConfig

    def start(self):
        r"""!Start the input source thread"""
        logging.debug("starting input thread")
        self._isRunning = True
        self._inputThread = threading.Thread(target=self._runThread, name="inputThread",
                                             args=(self._inputQueue, self._inputConfig, self._decoderConfig))
        self._inputThread.daemon = True
        self._inputThread.start()

    @abstractmethod
    def _runThread(self, dataQueue, sdrConfig, decoderConfig):
        r"""!Thread routine of the input source has to be inherit"""

    def shutdown(self):
        r"""!Stop the input source thread"""
        if self._isRunning:
            logging.debug("wait for stopping the input thread")
            self._isRunning = False
            self._inputThread.join()
            logging.debug("input thread stopped")

    def addToQueue(self, data):
        r"""!Decode and add alarm data to the queue for further processing during boswatch client"""
        bwPacket = Decoder.decode(data)
        if bwPacket is not None:
            self._inputQueue.put_nowait((bwPacket, time.time()))
            logging.debug("Added received data to queue")

    def getDecoderInstance(self, decoderConfig, StdIn):
        mmProc = ProcessManager(str(decoderConfig.get("path", default="multimon-ng")), textMode=True)
        if decoderConfig.get("fms", default=0):
            mmProc.addArgument("-a FMSFSK")
        if decoderConfig.get("zvei", default=0):
            mmProc.addArgument("-a ZVEI1")
        if decoderConfig.get("poc512", default=0):
            mmProc.addArgument("-a POCSAG512")
        if decoderConfig.get("poc1200", default=0):
            mmProc.addArgument("-a POCSAG1200")
        if decoderConfig.get("poc2400", default=0):
            mmProc.addArgument("-a POCSAG2400")
        if decoderConfig.get("char", default=0):
            mmProc.addArgument("-C " + str(decoderConfig.get("char")))
        mmProc.addArgument("-f alpha")
        mmProc.addArgument("-t raw -")
        mmProc.setStdin(StdIn)
        mmProc.setStderr(open(paths.LOG_PATH + "multimon-ng.log", "a"))
        return mmProc
