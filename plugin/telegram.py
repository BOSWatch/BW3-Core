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
@date:        14.01.2018
@author:      Bastian Schroll
@description: Template Plugin File
"""
import logging

from telegram.error import (TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError)
from plugin.pluginBase import PluginBase
import telegram
import re
import geocoder

# ###################### #
# Custom plugin includes #

# ###################### #

logging.debug("- %s loaded", __name__)


class BoswatchPlugin(PluginBase):
    """!Description of the Plugin"""

    def __init__(self, config):
        """!Do not change anything here!"""
        super().__init__(__name__, config)  # you can access the config class on 'self.config'

    def onLoad(self):
        """!Called by import of the plugin"""
        pass

    def setup(self):
        """!Called before alarm"""
        self.bot = telegram.Bot(token=self.config.get("botToken", default=""))
        pass

    def fms(self, bwPacket):
        """!Called on FMS alarm

        @param bwPacket: bwPacket instance"""
        logging.warning('Telegram Plugin does not work for FMS')
        pass

    def pocsag(self, bwPacket):
        """!Called on POCSAG alarm

        @param bwPacket: bwPacket instance"""

        try:
            # Send Message via Telegram
            msg = bwPacket.get("ric") + " (" + bwPacket.get("subric") + ")\n" + bwPacket.get("message")
            self.bot.send_message(chat_id=self.config.get("chatId", default=""), text=msg)

            # Send Location via Telegram if Geocoding is enabled and Provider and Key are set
            if self.config.get("geocoding", default=False):
                try:
                    address = re.search(self.config.get("geoRegex"), bwPacket.get("message"))[1]
                    provider = self.config.get("geoApiProvider")

                    if "mapbox" == provider:
                        g = geocoder.mapbox(address, key=self.config.get("geoApiToken"))
                    elif "google" == provider:
                        g = geocoder.google(address, key=self.config.get("geoApiToken"))
                    else:
                        return

                    (lat, lng) = g.latlng
                    self.bot.sendLocation(chat_id=self.config.get("chatId", default=""), latitude=lat, longitude=lng)
                except Exception:
                    logging.error('Error while sending location, please Check your geocoding provider and api-key')
        except Unauthorized:
            logging.error('Error while Telegram Message, please Check your api-key')
        except TimedOut or NetworkError:
            logging.error('Error while Telegram Message, please Check your connectivity')
        except BadRequest or TelegramError:
            logging.error('Error while Telegram Message')

        pass

    def zvei(self, bwPacket):
        """!Called on ZVEI alarm

        @param bwPacket: bwPacket instance"""
        logging.warning('Telegram Plugin does not work for ZVEI')
        pass

    def msg(self, bwPacket):
        """!Called on MSG packet

        @param bwPacket: bwPacket instance"""
        logging.warning('Telegram Plugin does not work for MSG')
        pass

    def teardown(self):
        """!Called after alarm"""
        pass

    def onUnload(self):
        """!Called by destruction of the plugin"""
        pass
