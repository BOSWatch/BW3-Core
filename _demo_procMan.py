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

#  ./multimon-ng -i -a POCSAG1200 -t raw /home/schrolli/Downloads/poc1200.raw

proc = ProcessManager("/opt/multimon/multimon-ng", textMode=True)
proc.addArgument("-i")
proc.addArgument("-a POCSAG1200")
proc.addArgument("-t raw")
proc.addArgument("./poc1200.raw")
proc.start()

proc.skipLines(5)
while proc.isRunning:
    line = proc.readline()
    if line is not "":
        Decoder.decode(line)


proc.stop()

