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

@file:        wildcard.py
@date:        15.01.2018
@author:      Bastian Schroll
@description: Little Helper to replace wildcards in stings
"""
import logging

# from boswatch.module import file

logging.debug("- %s loaded", __name__)


def replace(text, bwPacket):

    # static replacements
    text.replace("%BR%", "\r\n")
    text.replace("%LPAR%", "(").replace("%RPAR%", ")")

    # packet replacements
    text.replace("%MODE%", bwPacket.getField("mode"))
    text.replace("%FREQ%", bwPacket.getField("frequency"))

    # mode specific replacements
    # if bwPacket
