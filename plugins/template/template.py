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

@file:        template.py
@date:        14.01.2018
@author:      Bastian Schroll
@description: Template Plugin File
"""
import logging
from boswatch.plugin.plugin import Plugin

logging.debug("- %s loaded", __name__)


class BoswatchPlugin(Plugin):
    def __init__(self):
        """!Do not change anything here except the PLUGIN NAME in the super() call"""
        # PLEASE SET YOU PLUGIN NAME HERE !!!!
        super().__init__("template")

    def onLoad(self):
        """!Called by import of the plugin"""
        logging.debug("onLoad")

    def setup(self):
        """!Called before alarm"""
        logging.info(self.config.getStr("Example", "String"))

    def alarm(self, bwPacket):
        """!Called on alarm

        @param bwPacket: bwPacket instance"""
        logging.info(bwPacket)
        logging.info(self.config.getBool("Example", "bool"))

    def teardown(self):
        """!Called after alarm
        Must be inherit"""
        logging.info(self.config.getInt("Example", "integer"))

    def onUnload(self):
        logging.debug("onUnload")
        """!Called by destruction of the plugin"""
        pass
