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

@file:        netCheck.py
@date:        21.09.2018
@author:      Bastian Schroll
@description: Worker to check internet connection
"""
import logging
from urllib.request import urlopen

logging.debug("- %s loaded", __name__)


class NetCheck:
    """!Worker class to check internet connection"""

    def __init__(self, hostname="https://www.google.com/", timeout=1):
        self._hostname = hostname
        self._timeout = timeout

    def checkConn(self):
        try:
            urlopen(self._hostname, timeout=self._timeout)
            return True
        except:
            return False
