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

@file:        telegramdirty.py
@date:        06.06.2025
@author:      Claus Schichl
@description: Telegram dirty
"""
import logging
from plugin.pluginBase import PluginBase

# ###################### #
# Custom plugin includes #
import requests
# ###################### #

logging.debug("- %s loaded", __name__)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class BoswatchPlugin(PluginBase):
    """!Description of the Plugin"""
    def __init__(self, config):
        """!Do not change anything here!"""
        super().__init__(__name__, config)  # you can access the config class on 'self.config'

    def onLoad(self):
        """!Called by import of the plugin"""
        bot_token = self.config.get("botToken") #Import von Token aus config/server.yaml
        chat_id = self.config.get("chatIds") #Import von ChatIDs aus config/server.yaml
        nachricht = "Server up and running!"
        url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
        payload = {
            'chat_id': chat_id,
            'text': nachricht
        }
        response = requests.post(url, data=payload)

        if response.status_code == 200:
            print("Nachricht erfolgreich gesendet!")
        else:
            print("Fehler beim Senden:", response.text)
        pass



    def setup(self):
        """!Called before alarm
        Remove if not implemented"""
        pass

    def fms(self, bwPacket):
        """!Called on FMS alarm

        @param bwPacket: bwPacket instance
        Remove if not implemented"""
        pass

    def pocsag(self, bwPacket):
        """!Called on POCSAG alarm

        @param bwPacket: bwPacket instance
        Remove if not implemented"""
        pass

    def zvei(self, bwPacket):
        """!Called on ZVEI alarm
        @param bwPacket: bwPacket instance"""
        bot_token = self.config.get("botToken") #Import von Token aus config/server.yaml
        chat_id = self.config.get("chatIds") #Import von ChatIDs aus config/server.yaml
        nachricht = self.parseWildcards(self.config.get("message_zvei", default="{TONE}")) # Übergabe mit Wildcards aus config/server.yaml der "message_zvei", falls nicht definiert, Defaultwert
        #nachricht = bwPacket.get("clientName") + ": " + (bwPacket.get("description") or bwPacket.get("tone")) # Name vom Client und ": " und wenn Description vorhanden, ansonsten ZVEI
        url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
        payload = {
            'chat_id': chat_id,
            'text': nachricht
        }
        response = requests.post(url, data=payload)

        if response.status_code == 200:
            print("Nachricht erfolgreich gesendet!")
        else:
            print("Fehler beim Senden:", response.text)
        pass

    def msg(self, bwPacket):
        """!Called on MSG packet

        @param bwPacket: bwPacket instance
        Remove if not implemented"""
        pass

    def teardown(self):
        """!Called after alarm
        Remove if not implemented"""
        pass

    def onUnload(self):
        """!Called by destruction of the plugin
        Remove if not implemented"""
        pass