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
@date:        17.11.2025
@author:      Claus Schichl nach der Idee von Jan Speller
@description: Telegram-Plugin mit Retry-Logik ohne externe Telegram-Abhängigkeiten
"""

import logging
import time
import threading
import queue
import requests
from plugin.pluginBase import PluginBase

# Setup Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# ===========================
# TelegramSender-Class
# ===========================

class TelegramSender:
    def __init__(self, bot_token, chat_ids, max_retries=None, initial_delay=None, max_delay=None, parse_mode=None):
        self.bot_token = bot_token
        self.chat_ids = chat_ids
        self.max_retries = max_retries if max_retries is not None else 5
        self.initial_delay = initial_delay if initial_delay is not None else 2
        self.max_delay = max_delay if max_delay is not None else 300
        self.parse_mode = parse_mode
        self.msg_queue = queue.Queue()
        self._worker = threading.Thread(target=self._worker_loop, daemon=True)
        self._worker.start()

    def send_message(self, text):
        for chat_id in self.chat_ids:
            self.msg_queue.put(("text", chat_id, text, 0))  # retry_count = 0

    def send_location(self, latitude, longitude):
        for chat_id in self.chat_ids:
            self.msg_queue.put(("location", chat_id, {"latitude": latitude, "longitude": longitude}, 0))

    def _worker_loop(self):
        delay = self.initial_delay

        while True:
            try:
                msg_type, chat_id, content, retry_count = self.msg_queue.get()

                success, permanent_failure, custom_delay = self._send_to_telegram(msg_type, chat_id, content)

                if success:
                    delay = self.initial_delay

                elif permanent_failure:
                    logger.error("Permanenter Fehler – Nachricht wird verworfen.")

                elif retry_count >= self.max_retries:
                    logger.error("Maximale Wiederholungsanzahl erreicht – Nachricht wird verworfen.")

                else:
                    logger.warning(f"Erneutes Einreihen der Nachricht (Versuch {retry_count + 1}).")
                    self.msg_queue.put((msg_type, chat_id, content, retry_count + 1))

                    # use the Telegram-provided value (retry_after) if available
                    wait_time = custom_delay if custom_delay is not None else delay
                    time.sleep(wait_time)

                    # increase delay for the next attempt (exponential backoff)
                    delay = min(delay * 2, self.max_delay)

            except Exception as e:
                logger.exception(f"Fehler im Telegram-Worker: {e}")
                time.sleep(5)

    def _send_to_telegram(self, msg_type, chat_id, content):
        if msg_type == "text":
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload = {
                'chat_id': chat_id,
                'text': content,
            }
            if self.parse_mode:
                payload['parse_mode'] = self.parse_mode
        elif msg_type == "location":
            url = f"https://api.telegram.org/bot{self.bot_token}/sendLocation"
            payload = {
                'chat_id': chat_id,
                **content
            }
        else:
            logger.error("Unbekannter Nachrichtentyp.")
            return False, True, None  # unknown message type = permanent failure

        try:
            custom_delay = None  # standardvalue for return, except in case of 429

            response = requests.post(url, data=payload, timeout=10)

            if response.status_code == 429:
                custom_delay = response.json().get("parameters", {}).get("retry_after", 5)
                logger.warning(f"Rate Limit erreicht – warte {custom_delay} Sekunden.")
                return False, False, custom_delay  # Telegram gives exact wait time

            if response.status_code == 400:
                logger.error("Ungültige Parameter – Nachricht wird nicht erneut gesendet.")
                return False, True, custom_delay  # permanent failure

            if response.status_code == 401:
                logger.critical("Ungültiger Bot-Token – bitte prüfen!")
                return False, True, custom_delay  # permanent failure

            response.raise_for_status()
            logger.info(f"Erfolgreich gesendet an Chat-ID {chat_id}")
            return True, False, custom_delay

        except requests.RequestException as e:
            logger.warning(f"Fehler beim Senden an Telegram (Chat-ID {chat_id}): {e}")
            return False, False, custom_delay


# ===========================
# BoswatchPlugin-Class
# ===========================


class BoswatchPlugin(PluginBase):
    def __init__(self, config):
        r"""!Do not change anything here!"""
        super().__init__(__name__, config)  # you can access the config class on 'self.config'

    def onLoad(self):
        r"""!Called by import of the plugin"""
        bot_token = self.config.get("botToken")
        chat_ids = self.config.get("chatIds", default=[])

        if not bot_token or not chat_ids:
            logger.error("botToken oder chatIds fehlen in der Konfiguration!")
            return

        # configurable parameters with fallback defaults
        max_retries = self.config.get("max_retries")
        initial_delay = self.config.get("initial_delay")
        max_delay = self.config.get("max_delay")
        parse_mode = self.config.get("parse_mode")

        self.sender = TelegramSender(
            bot_token=bot_token,
            chat_ids=chat_ids,
            max_retries=max_retries,
            initial_delay=initial_delay,
            max_delay=max_delay,
            parse_mode=parse_mode
        )

        startup_message = self.config.get("startup_message")
        if startup_message and startup_message.strip():
            self.sender.send_message(startup_message)

    def setup(self):
        r"""!Called before alarm
        Remove if not implemented"""
        pass

    def fms(self, bwPacket):
        r"""!Called on FMS alarm
        @param bwPacket: bwPacket instance"""
        msg = self.parseWildcards(self.config.get("message_fms", default="{FMS}"))
        self.sender.send_message(msg)

    def pocsag(self, bwPacket):
        r"""!Called on POCSAG alarm
        @param bwPacket: bwPacket instance"""
        msg = self.parseWildcards(self.config.get("message_pocsag", default="{RIC}({SRIC})\n{MSG}"))
        self.sender.send_message(msg)

        if bwPacket.get("lat") is not None and bwPacket.get("lon") is not None:
            lat, lon = bwPacket.get("lat"), bwPacket.get("lon")
            logger.debug("Koordinaten gefunden – sende Standort.")
            self.sender.send_location(lat, lon)

    def zvei(self, bwPacket):
        r"""!Called on ZVEI alarm
        @param bwPacket: bwPacket instance"""
        msg = self.parseWildcards(self.config.get("message_zvei", default="{TONE}"))
        self.sender.send_message(msg)

    def msg(self, bwPacket):
        r"""!Called on MSG packet
        @param bwPacket: bwPacket instance"""
        msg = self.parseWildcards(self.config.get("message_msg"))
        self.sender.send_message(msg)

    def teardown(self):
        r"""!Called after alarm
        Remove if not implemented"""
        pass

    def onUnload(self):
        r"""!Called by destruction of the plugin
        Remove if not implemented"""
        pass
