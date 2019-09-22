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

@file:        template_module.py
@date:        01.03.2019
@author:      Bastian Schroll
@description: Template Module File
"""
import logging
from module.module import Module

# ###################### #
# Custom plugin includes #

# ###################### #

logging.debug("- %s loaded", __name__)


class BoswatchModule(Module):
    """!Description of the Module"""
    def __init__(self, config):
        """!Do not change anything here!"""
        super().__init__(__name__, config)  # you can access the config class on 'self.config'

    def onLoad(self):
        """!Called by import of the plugin"""
        pass

    def doWork(self, bwPacket):
        """!start an run of the module.

        @param bwPacket: A BOSWatch packet instance
        @return bwPacket or False"""
        return bwPacket

    def onUnload(self):
        """!Called by destruction of the plugin"""
        pass
