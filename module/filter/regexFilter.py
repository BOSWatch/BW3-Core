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

@file:        regexFilter.py
@date:        26.10.2019
@author:      Bastian Schroll
@description: Regex filter module
"""
import logging
from module.moduleBase import ModuleBase

# ###################### #
# Custom plugin includes #
import re
# ###################### #

logging.debug("- %s loaded", __name__)


class BoswatchModule(ModuleBase):
    r"""!Regex based filter mechanism"""
    def __init__(self, config):
        r"""!Do not change anything here!"""
        super().__init__(__name__, config)  # you can access the config class on 'self.config'

    def onLoad(self):
        r"""!Called by import of the plugin"""
        pass

    def doWork(self, bwPacket):
        r"""!start an run of the module.

        @param bwPacket: A BOSWatch packet instance"""
        for regexFilter in self.config:
            checkFailed = False
            logging.debug("try filter '%s' with %d check(s)", regexFilter.get("name"), len(regexFilter.get("checks")))

            for check in regexFilter.get("checks"):
                fieldData = bwPacket.get(check.get("field"))

                if not fieldData or not re.search(check.get("regex"), fieldData):
                    logging.debug("[-] field '%s' with regex '%s'", check.get("field"), check.get("regex"))
                    checkFailed = True
                    break  # if one check failed we break this filter
                else:
                    logging.debug("[+] field '%s' with regex '%s'", check.get("field"), check.get("regex"))

            if not checkFailed:
                logging.debug("[PASSED] filter '%s'", regexFilter.get("name"))
                return None  # None -> Router will go on with this packet
            logging.debug("[FAILED] filter '%s'", regexFilter.get("name"))

        return False  # False -> Router will stop further processing

    def onUnload(self):
        r"""!Called by destruction of the plugin"""
        pass
