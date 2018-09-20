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

# ###################### #
# Custom plugin includes #

# ###################### #

logging.debug("- %s loaded", __name__)


class BoswatchPlugin(Plugin):
    """!Description of the Plugin"""
    def __init__(self):
        """!Do not change anything here except the PLUGIN NAME in the super() call"""
        # PLEASE SET YOU PLUGIN NAME HERE !!!!
        Plugin.__init__("template")

    def onLoad(self):
        """!Called by import of the plugin"""
        pass

    def setup(self):
        """!Called before alarm"""
        pass

    def fms(self, bwPacket):
        """!Called on FMS alarm

        @param bwPacket: bwPacket instance"""
        pass

    def pocsag(self, bwPacket):
        """!Called on POCSAG alarm

        @param bwPacket: bwPacket instance"""
        pass

    def zvei(self, bwPacket):
        """!Called on ZVEI alarm

        @param bwPacket: bwPacket instance"""

    def msg(self, bwPacket):
        """!Called on MSG packet

        @param bwPacket: bwPacket instance"""

    def teardown(self):
        """!Called after alarm"""
        pass

    def onUnload(self):
        """!Called by destruction of the plugin"""
        pass
