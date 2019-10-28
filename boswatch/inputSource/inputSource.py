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

@file:        sdrInput.py
@date:        28.10.2018
@author:      Bastian Schroll
@description: Input source for sdr with rtl_fm
"""
import time
import logging
import threading
from boswatch.utils import paths
from boswatch.processManager import ProcessManager

logging.debug("- %s loaded", __name__)


class SdrInput:
    """!Worker class to check internet connection"""

    def __init__(self):
        self._isRunning = False
        self._mmThread = None

    def start(self, packetQueue, inputConfig, decoderConfig):
        self._isRunning = True
        self._mmThread = threading.Thread(target=self._handleSDRInput, name="mmReader",
                                          args=(packetQueue, inputConfig, decoderConfig))
        self._mmThread.daemon = True
        self._mmThread.start()

    def shutdown(self):
        self._isRunning = False
        self._mmThread.join()

    def _handleSDRInput(self, dataQueue, sdrConfig, decoderConfig):  # todo exception handling inside
        sdrProc = ProcessManager(str(sdrConfig.get("rtlPath", default="rtl_fm")))
        sdrProc.addArgument("-d " + str(sdrConfig.get("device", default="0")))     # device id
        sdrProc.addArgument("-f " + sdrConfig.get("frequency"))                    # frequencies
        sdrProc.addArgument("-p " + str(sdrConfig.get("error", default="0")))      # frequency error in ppm
        sdrProc.addArgument("-l " + str(sdrConfig.get("squelch", default="1")))    # squelch
        sdrProc.addArgument("-g " + str(sdrConfig.get("gain", default="100")))     # gain
        sdrProc.addArgument("-M fm")                                               # set mode to fm
        sdrProc.addArgument("-E DC")                                               # set DC filter
        sdrProc.addArgument("-s 22050")                                            # bit rate of audio stream
        sdrProc.setStderr(open(paths.LOG_PATH + "rtl_fm.log", "a"))
        sdrProc.start()

        mmProc = ProcessManager(str(sdrConfig.get("mmPath", default="multimon-ng")), textMode=True)
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
        mmProc.addArgument("-f alpha")
        mmProc.addArgument("-t raw -")
        mmProc.setStdin(sdrProc.stdout)
        mmProc.setStderr(open(paths.LOG_PATH + "multimon-ng.log", "a"))
        mmProc.start()

        logging.info("start decoding")
        while self._isRunning:
            if not sdrProc.isRunning:
                logging.warning("rtl_fm was down - try to restart")
                sdrProc.start()
            elif not mmProc.isRunning:
                logging.warning("multimon was down - try to restart")
                mmProc.start()
            elif sdrProc.isRunning and mmProc.isRunning:
                line = mmProc.readline()
                if line:
                    dataQueue.put_nowait((line, time.time()))
                    logging.debug("Add data to queue")
                    print(line)
        logging.debug("stopping thread")
        mmProc.stop()
        sdrProc.stop()
