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

    def msg_send(self, bwPacket, msg_payload):
        """!Funktion zum Senden einer Nachricht über Telegram
        @param bwPacket: bwPacket instance
        @param msg_payload: Nachrichtentext, der gesendet werden soll"""
        
        bot_token = self.config.get("botToken")
        chat_id = self.config.get("chatIds")

        url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
        payload = {
            'chat_id': chat_id,
            'text': msg_payload
        }

        response = requests.post(url, data=payload)

        if response.status_code == 200:
            print("Nachricht erfolgreich gesendet!")
        else:
            print("Fehler beim Senden:", response.text)

    def onLoad(self):
        """!Called by import of the plugin"""
        msg_payload = "Server up and running!"
        self.msg_send(None, msg_payload)
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
        msg_payload = self.parseWildcards(
            self.config.get("message_zvei", default="{TONE}") # Übergabe mit Wildcards aus config/server.yaml der "message_zvei", falls nicht definiert, Defaultwert
        )
        self.msg_send(bwPacket, msg_payload)
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
