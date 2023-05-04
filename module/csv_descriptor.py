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

@file:        csv_descriptor.py
@date:        01.05.2023
@author:      nevrrmind
@description: Module to add descriptions to bwPackets from a csv-file.
"""
import logging
from module.moduleBase import ModuleBase

# ###################### #
# Custom plugin includes #
import csv
# ###################### #

logging.debug("- %s loaded", __name__)


class BoswatchModule(ModuleBase):
    """!Adds descriptions to bwPackets"""
    def __init__(self, config):
        """!Do not change anything here!"""
        super().__init__(__name__, config)  # you can access the config class on 'self.config'

    def onLoad(self):
        """!Called by import of the plugin"""
        self.registerWildcard(self.config.get("wildcard"), self.config.get("descrField"))
        poccsv = self.config.get("csvfile")
        logging.debug("POCCSV-File-Path '%s'", poccsv)
        with open(poccsv, mode='r') as inp:
            reader = csv.reader(inp)
            self.poc_csv_dict = {rows[0]: rows[1] for rows in reader}

    def doWork(self, bwPacket):
        """!start an run of the module.

        @param bwPacket: A BOSWatch packet instance"""
        kenner_ric = bwPacket.get("ric")
        if str(kenner_ric) in self.poc_csv_dict:
            kenner = self.poc_csv_dict[kenner_ric]
            logging.debug("Description '%s' added in packet field '%s'", kenner, self.config.get("descrField"))
            bwPacket.set(self.config.get("descrField"), kenner)
        else:
            kenner = "Unbekannt"
            logging.debug("Description '%s' added in packet field '%s'", kenner, self.config.get("descrField"))
            bwPacket.set(self.config.get("descrField"), kenner)
        return bwPacket

    def onUnload(self):
        """!Called by destruction of the plugin"""
        pass
