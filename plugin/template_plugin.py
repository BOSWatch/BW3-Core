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

@file:        template_plugin.py
@date:        14.01.2018
@author:      Bastian Schroll
@description: Template Plugin File
"""
import logging
from plugin.pluginBase import PluginBase

# ###################### #
# Custom plugin includes #

# ###################### #

logging.debug("- %s loaded", __name__)


class BoswatchPlugin(PluginBase):
    r"""!Description of the Plugin"""
    def __init__(self, config):
        r"""!Do not change anything here!"""
        super().__init__(__name__, config)  # you can access the config class on 'self.config'

    def onLoad(self):
        r"""!Called by import of the plugin
        Remove if not implemented"""
        pass

    def setup(self):
        r"""!Called before alarm
        Remove if not implemented"""
        pass

    def fms(self, bwPacket):
        r"""!Called on FMS alarm

        @param bwPacket: bwPacket instance
        Remove if not implemented"""
        pass

    def pocsag(self, bwPacket):
        r"""!Called on POCSAG alarm

        @param bwPacket: bwPacket instance
        Remove if not implemented"""
        pass

    def zvei(self, bwPacket):
        r"""!Called on ZVEI alarm

        @param bwPacket: bwPacket instance
        Remove if not implemented"""
        pass

    def msg(self, bwPacket):
        r"""!Called on MSG packet

        @param bwPacket: bwPacket instance
        Remove if not implemented"""
        pass

    def teardown(self):
        r"""!Called after alarm
        Remove if not implemented"""
        pass

    def onUnload(self):
        r"""!Called by destruction of the plugin
        Remove if not implemented"""
        pass
