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

@file:        watchdog.py
@date:        ##.##.2018
@author:      Bastian Schroll
@description: Watchdog to _check if BOSWatch client, server, rtl_fm or multimon-ng is still running
"""

import logging

logging.debug("- %s loaded", __name__)


class Watchdog:
    """!Class for an Watchdog to observe,
    if needed subprocess still running"""

    def __init__(self):
        """!Create a new instance"""
        pass
