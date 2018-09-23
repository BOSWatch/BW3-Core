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
        """!Create a new NetCheck instance

        @param hostname: host against connection check is running ("https://www.google.com/")
        @param timout: timout for connection check in sec. (1)"""
        self._hostname = hostname
        self._timeout = timeout
        self._connectionState = False
        self.checkConn()  # initiate a first check

    def checkConn(self):
        """!Check the connection

        @return True or False"""
        try:
            urlopen(self._hostname, timeout=self._timeout)
            logging.debug("%s is reachable", self._hostname)
            self._connectionState = True
            return True
        except:
            logging.warning("%s is not reachable", self._hostname)
            self._connectionState = False
            return False

    @property
    def connectionState(self):
        """!Property for the last connection state from checkConn()"""
        return self._connectionState
