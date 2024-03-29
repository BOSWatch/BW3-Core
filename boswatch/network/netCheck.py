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

@file:        netCheck.py
@date:        21.09.2018
@author:      Bastian Schroll
@description: Worker to check internet connection
"""
import logging
from urllib.request import urlopen

logging.debug("- %s loaded", __name__)


class NetCheck:
    r"""!Worker class to check internet connection"""

    def __init__(self, hostname="https://www.google.com/", timeout=1):
        r"""!Create a new NetCheck instance

        @param hostname: host against connection check is running ("https://www.google.com/")
        @param timeout: timeout for connection check in sec. (1)"""
        self._hostname = hostname
        self._timeout = timeout
        self.connectionState = False
        self.checkConn()  # initiate a first check

    def checkConn(self):
        r"""!Check the connection

        @return True or False"""
        try:
            urlopen(self._hostname, timeout=self._timeout)
            logging.debug("%s is reachable", self._hostname)
            self.connectionState = True
            return True
        except:  # todo find right exception type
            logging.warning("%s is not reachable", self._hostname)
            self.connectionState = False
            return False
