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

@file:        pulseaudioInput.py
@date:        18.04.2020, 29.06.2020
@author:      Philipp von Kirschbaum, b-watch
@description: Input source for PulseAudio
"""
import logging
from boswatch.utils import paths
from boswatch.processManager import ProcessManager
from boswatch.inputSource.inputBase import InputBase

logging.debug("- %s loaded", __name__)


class PulseAudioInput(InputBase):
    """!Class for the PulseAudio input source"""

    def _runThread(self, dataQueue, PulseAudioConfig, decoderConfig):
        PulseAudioProc = None
        mmProc = None
        try:
            PulseAudioProc = ProcessManager("parec")
            PulseAudioProc.addArgument("--channels=1")                            # supress any other outputs
            PulseAudioProc.addArgument("--format=s16le")                          # set output format (16bit)
            PulseAudioProc.addArgument("--rate=22050")                            # set output sampling rate (22050Hz)
            PulseAudioProc.addArgument("--device=" +
                                       str(PulseAudioConfig.get("device", default="boswatch")) +
                                       ".monitor")                                # sink name
            PulseAudioProc.setStderr(open(paths.LOG_PATH + "pulseaudio.log", "a"))
            PulseAudioProc.start()

            mmProc = self.startmm(decoderConfig)
            mmProc.setStdin(PulseAudioProc.stdout)
            mmProc.setStderr(open(paths.LOG_PATH + "multimon-ng.log", "a"))
            mmProc.start()

            logging.info("start decoding")
            while self._isRunning:
                if not PulseAudioProc.isRunning:
                    logging.warning("PulseAudio was down - try to restart")
                    PulseAudioProc.start()
                elif not mmProc.isRunning:
                    logging.warning("multimon was down - try to restart")
                    mmProc.start()
                elif PulseAudioProc.isRunning and mmProc.isRunning:
                    line = mmProc.readline()
                    if line:
                        self.addToQueue(line)
        except:
            logging.exception("error in PulseAudio input routine")
        finally:
            mmProc.stop()
            PulseAudioProc.stop()
