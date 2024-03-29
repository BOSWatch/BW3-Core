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

@file:        modeFilter.py
@date:        09.03.2019
@author:      Bastian Schroll
@description: Filter module for the packet type
"""
import logging
from module.moduleBase import ModuleBase

# ###################### #
# Custom plugin includes #

# ###################### #

logging.debug("- %s loaded", __name__)


class BoswatchModule(ModuleBase):
    r"""!Filter of specific bwPacket mode"""
    def __init__(self, config):
        r"""!Do not change anything here!"""
        super().__init__(__name__, config)  # you can access the config class on 'self.config'

    def onLoad(self):
        r"""!Called by import of the plugin"""
        pass

    def doWork(self, bwPacket):
        r"""!start an run of the module.

        @param bwPacket: A BOSWatch packet instance"""

        for mode in self.config.get("allowed", default=[]):
            if bwPacket.get("mode") == mode:
                logging.debug("mode is allowed: %s", bwPacket.get("mode"))
                return None
        logging.debug("mode is denied: %s", bwPacket.get("mode"))
        return False

    def onUnload(self):
        r"""!Called by destruction of the plugin"""
        pass
