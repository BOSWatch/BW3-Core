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

@file:        telegram.py
@date:        20.02.2020
@author:      Jan Speller
@description: Telegram Plugin
"""
import logging
from plugin.pluginBase import PluginBase

# ###################### #
# Custom plugin includes #
from telegram.error import (TelegramError, Unauthorized, BadRequest, TimedOut, NetworkError)
from telegram.ext import messagequeue as mq
from telegram.utils.request import Request
import telegram.bot
# ###################### #

logging.debug("- %s loaded", __name__)


class MQBot(telegram.bot.Bot):
    '''A subclass of Bot which delegates send method handling to MQ'''

    def __init__(self, *args, is_queued_def=True, mqueue=None, **kwargs):
        super(MQBot, self).__init__(*args, **kwargs)
        # below 2 attributes should be provided for decorator usage
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = mqueue or mq.MessageQueue()

    def __del__(self):
        try:
            self._msg_queue.stop()
        except:
            pass

    @mq.queuedmessage
    def send_message(self, *args, **kwargs):
        '''Wrapped method would accept new `queued` and `isgroup`
        OPTIONAL arguments'''
        return super(MQBot, self).send_message(*args, **kwargs)


class BoswatchPlugin(PluginBase):
    r"""!Description of the Plugin"""

    def __init__(self, config):
        r"""!Do not change anything here!"""
        super().__init__(__name__, config)  # you can access the config class on 'self.config'

    def onLoad(self):
        r"""!Called by import of the plugin"""
        if self.config.get("queue", default=True):
            q = mq.MessageQueue()
            request = Request(con_pool_size=8)
            self.bot = MQBot(token=self.config.get("botToken", default=""), request=request, mqueue=q)
            print('queue')
        else:
            self.bot = telegram.Bot(token=self.config.get("botToken"))
            print('normal')

    def fms(self, bwPacket):
        r"""!Called on FMS alarm

        @param bwPacket: bwPacket instance"""
        msg = self.parseWildcards(self.config.get("message_fms", default="{FMS}"))
        self._sendMessage(msg)

    def pocsag(self, bwPacket):
        r"""!Called on POCSAG alarm

        @param bwPacket: bwPacket instance"""
        msg = self.parseWildcards(self.config.get("message_pocsag", default="{RIC}({SRIC})\n{MSG}"))
        self._sendMessage(msg)

        if bwPacket.get("lat") is not None and bwPacket.get("lon") is not None:
            logging.debug("Found coordinates in packet")
            (lat, lon) = (bwPacket.get("lat"), bwPacket.get("lon"))
            self._sendLocation(lat, lon)

    def zvei(self, bwPacket):
        r"""!Called on ZVEI alarm

        @param bwPacket: bwPacket instance"""
        msg = self.parseWildcards(self.config.get("message_zvei", default="{TONE}"))
        self._sendMessage(msg)

    def msg(self, bwPacket):
        r"""!Called on MSG packet

        @param bwPacket: bwPacket instance"""
        msg = self.parseWildcards(self.config.get("message_msg"))
        self._sendMessage(msg)

    def _sendMessage(self, message):
        for chatId in self.config.get("chatIds", default=[]):
            try:
                # Send Message via Telegram
                logging.info("Sending message to " + chatId)
                self.bot.send_message(chat_id=chatId, text=message)

            except Unauthorized:
                logging.exception("Error while sending Telegram Message, please Check your api-key")
            except (TimedOut, NetworkError):
                logging.exception("Error while sending Telegram Message, please Check your connectivity")
            except (BadRequest, TelegramError):
                logging.exception("Error while sending Telegram Message")
            except Exception as e:
                logging.exception("Unknown Error while sending Telegram Message: " + str(type(e).__name__) + ": " + str(e))

    def _sendLocation(self, lat, lon):
        for chatId in self.config.get("chatIds", default=[]):
            try:
                # Send Location via Telegram
                if lat is not None and lon is not None:
                    logging.info("Sending location to " + chatId)
                    self.bot.sendLocation(chat_id=chatId, latitude=lat, longitude=lon)

            except Unauthorized:
                logging.exception("Error while sending Telegram Message, please Check your api-key")
            except (TimedOut, NetworkError):
                logging.exception("Error while sending Telegram Message, please Check your connectivity")
            except (BadRequest, TelegramError):
                logging.exception("Error while sending Telegram Message")
            except Exception as e:
                logging.exception("Unknown Error while sending Telegram Message: " + str(type(e).__name__) + ": " + str(e))
