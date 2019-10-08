#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    ____  ____  ______       __      __       __       _____
   / __ )/ __ \/ ___/ |     / /___ _/ /______/ /_     |__  /
  / __  / / / /\__ \| | /| / / __ `/ __/ ___/ __ \     /_ <
 / /_/ / /_/ /___/ /| |/ |/ / /_/ / /_/ /__/ / / /   ___/ /
/_____/\____//____/ |__/|__/\__,_/\__/\___/_/ /_/   /____/
                German BOS Information Script
                     by Bastian Schroll
"""

from boswatch.processManager import ProcessManager
from boswatch.decoder.decoder import Decoder
import logging.config
logging.config.fileConfig("config/logger_client.ini")

sdrProc = ProcessManager("/usr/bin/rtl_fm")
sdrProc.addArgument("-f 85M")
sdrProc.addArgument("-m fm")
sdrProc.start(True)

mmProc = ProcessManager("/opt/multimon/multimon-ng", textMode=True)
# mmProc.addArgument("-i")
# mmProc.addArgument("-a POCSAG1200 -a FMSFSK -a ZVEI1")
mmProc.addArgument("-f aplha")
mmProc.addArgument("-t raw /dev/stdin -")
mmProc.setStdin(sdrProc.stdout)
mmProc.start(True)
mmProc.skipLines(5)
while 1:
    if not mmProc.isRunning:
        logging.warning("multimon was down - try to restart")
        mmProc.start()
        mmProc.skipLines(5)
    line = mmProc.readline()
    if line:
        print(line)
