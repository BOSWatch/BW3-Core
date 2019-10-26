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

@file:        version.py
@date:        14.12.2017
@author:      Bastian Schroll
@description: Version numbers, branch and release date of BOSWatch
"""
import logging

logging.debug("- %s loaded", __name__)

client = {"major": 3, "minor": 0, "patch": 0}
server = {"major": 3, "minor": 0, "patch": 0}
date = {"day": 1, "month": 1, "year": 2019}
branch = "develop"
