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

@file:        alarmWorker.py
@date:        20.09.2018
@author:      Bastian Schroll
@description: Alarm worker to process the alarms in a separate thread
"""
import logging

# from boswatch.module import file

logging.debug("- %s loaded", __name__)


class alarmWorker:
    """!Worker class to process alarms"""

    def __init__(self, alarmQueue):
        self.__alarmQueue = alarmQueue
