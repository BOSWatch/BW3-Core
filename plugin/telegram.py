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
@date:        17.01.2026
@author:      Claus Schichl
@description: Telegram-Plugin
"""

import logging
import time
import threading
import queue
import requests
import re
from plugin.pluginBase import PluginBase

# Setup logging
logger = logging.getLogger(__name__)


# ===========================
# TelegramSender-Class
# ===========================

class TelegramSender:
    def __init__(self, bot_token, chat_ids, max_retries=None, initial_delay=None, max_delay=None, parse_mode=None):
        self._stop_event = threading.Event()
        self.bot_token = bot_token
        self.chat_ids = chat_ids
        self.max_retries = max_retries if max_retries is not None else 5
        self.initial_delay = initial_delay if initial_delay is not None else 2
        self.max_delay = max_delay if max_delay is not None else 300
        self.msg_queue = queue.Queue(maxsize=100)  # max 100 messages
        self.parse_mode = parse_mode

        # Start Worker Thread
        self._worker = threading.Thread(target=self._worker_loop, daemon=True)
        self._worker.start()

    def send_message(self, text):
        clean_text = self._escape_text(text, self.parse_mode)
        for chat_id in self.chat_ids:
            try:
                self.msg_queue.put(("text", chat_id, clean_text, 0), block=False)
            except queue.Full:
                logger.error(f"Message queue full for chat_id {chat_id}, message discarded: {clean_text[:50]}...")

    def send_location(self, latitude, longitude):
        try:
            # Use validated float values, not original strings
            lat = float(latitude)
            lon = float(longitude)
            # check Telegram API Limits
            if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                logger.error(f"Invalid coordinates: lat={lat}, lon={lon} (out of range)")
                return
        except (TypeError, ValueError) as e:
            logger.error(f"Invalid coordinate format: {e}, location skipped")
            return

        for chat_id in self.chat_ids:
            try:
                self.msg_queue.put(("location", chat_id, {"latitude": lat, "longitude": lon}, 0), block=False)
            except queue.Full:
                logger.error(f"Location queue full for chat_id {chat_id}, location discarded: {lat}, {lon}")

    @staticmethod
    def _escape_text(text, parse_mode):
        if not text:
            return ""
        if parse_mode == "HTML":
            protected_tags = {}
            tag_pattern = r'<(/?)(\w+)>'
            allowed = ["b", "strong", "i", "em", "code", "pre", "u", "s"]

            def protect_tag(match):
                tag_full = match.group(0)
                tag_name = match.group(2)
                if tag_name in allowed:
                    placeholder = f"__TAG_{len(protected_tags)}__"
                    protected_tags[placeholder] = tag_full
                    return placeholder
                return tag_full

            text = re.sub(tag_pattern, protect_tag, text)
            text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            for placeholder, original_tag in protected_tags.items():
                text = text.replace(placeholder, original_tag)
        elif parse_mode == "MarkdownV2":
            # Escape all MarkdownV2 special characters (Telegram API requirement)
            # See: https://core.telegram.org/bots/api#markdownv2-style
            escape_chars = r'_*[]()~`>#+-=|{}.!'
            text = "".join(['\\' + char if char in escape_chars else char for char in text])
        return text[:4090] + "[...]" if len(text) > 4096 else text

    def _worker_loop(self):
        delay = self.initial_delay
        while not self._stop_event.is_set():
            try:
                msg_type, chat_id, content, retry_count = self.msg_queue.get(timeout=1)
                success, permanent_failure, custom_delay, error_details = self._send_to_telegram(msg_type, chat_id, content)
                if success:
                    delay = self.initial_delay
                elif permanent_failure or retry_count >= self.max_retries:
                    logger.warning(f"Discarding message for {chat_id}: {error_details}")
                else:
                    wait_time = custom_delay if custom_delay is not None else delay
                    time.sleep(wait_time)
                    self.msg_queue.put((msg_type, chat_id, content, retry_count + 1))
                    delay = min(delay * 2, self.max_delay)
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Error in Telegram worker: {e}")
                time.sleep(5)

    def _send_to_telegram(self, msg_type, chat_id, content):
        url = f"https://api.telegram.org/bot{self.bot_token}/"
        url += "sendMessage" if msg_type == "text" else "sendLocation"
        payload = {'chat_id': chat_id}

        if msg_type == "text":
            payload['text'] = content
            if self.parse_mode:
                payload['parse_mode'] = self.parse_mode
        else:
            payload.update(content)

        try:
            response = requests.post(url, data=payload, timeout=10)
            if response.status_code == 200:
                logger.info(f"Successfully sent to Chat-ID {chat_id}")
                return True, False, None, None

            # Rate limiting
            if response.status_code == 429:
                retry_after = response.json().get("parameters", {}).get("retry_after", 5)
                logger.warning(f"Rate limited for {chat_id}, retry after {retry_after}s")
                return False, False, retry_after, f"Rate Limit (retry after {retry_after}s)"

            return False, response.status_code < 500, None, f"HTTP {response.status_code}"
        except Exception as e:
            return False, False, None, str(e)

    def shutdown(self):
        r"""Graceful shutdown with queue draining"""
        logger.info("Shutting down Telegram sender...")
        self._stop_event.set()
        timeout = time.time() + 5
        while not self.msg_queue.empty() and time.time() < timeout:
            time.sleep(0.1)
        remaining = self.msg_queue.qsize()
        if remaining > 0:
            logger.warning(f"{remaining} messages in queue discarded during shutdown")
        self._worker.join(timeout=5)


# ===========================
# BoswatchPlugin-Class
# ===========================

logging.debug("- %s loaded", __name__)


class BoswatchPlugin(PluginBase):
    r"""!Description of the Plugin"""
    def __init__(self, config):
        r"""!Do not change anything here!"""
        super().__init__(__name__, config)  # you can access the config class on 'self.config'

    def _ensure_sender(self):
        r""" checking with hasattr if self.sender already exists"""
        if not hasattr(self, 'sender') or self.sender is None:
            token = self.config.get("botToken")
            ids = self.config.get("chatIds", default=[])

            if token and ids:
                self.sender = TelegramSender(
                    bot_token=token,
                    chat_ids=ids,
                    max_retries=self.config.get("max_retries"),
                    initial_delay=self.config.get("initial_delay"),
                    max_delay=self.config.get("max_delay"),
                    parse_mode=self.config.get("parse_mode")
                )
                logger.debug("TelegramSender initialized via Self-Healing")
            else:
                missing = []
                if not token:
                    missing.append("botToken")
                if not ids:
                    missing.append("chatIds")
                logger.error(f"Telegram configuration incomplete! Missing: {', '.join(missing)}. Plugin will not send messages.")

    def _has_sender(self):
        r"""Check if sender is available and properly initialized"""
        return hasattr(self, 'sender') and self.sender is not None

    def onLoad(self):
        r"""!Called by import of the plugin"""
        self._ensure_sender()
        if not self._has_sender():
            logger.warning("Telegram plugin loaded but not configured.  Messages will be discarded.")
        else:
            startup = self.config.get("startup_message")
            if startup and startup.strip():
                self.sender.send_message(startup)

    def setup(self):
        r"""!Called before alarm"""
        # ensure sender exists before alarms are processed
        self._ensure_sender()

    def fms(self, bwPacket):
        r"""!Called on FMS alarm"""
        if self._has_sender():
            msg = self.parseWildcards(self.config.get("message_fms", default="{FMS}"))
            self.sender.send_message(msg)

    def pocsag(self, bwPacket):
        r"""!Called on POCSAG alarm"""
        if self._has_sender():
            msg = self.parseWildcards(self.config.get("message_pocsag", default="{RIC}({SRIC})\n{MSG}"))
            self.sender.send_message(msg)

            if self.config.get("coordinates", default=False):
                lat = bwPacket.get("lat")
                lon = bwPacket.get("lon")
                if lat is not None and lon is not None:
                    self.sender.send_location(lat, lon)

    def zvei(self, bwPacket):
        r"""!Called on ZVEI alarm"""
        if self._has_sender():
            msg = self.parseWildcards(self.config.get("message_zvei", default="{TONE}"))
            self.sender.send_message(msg)

    def msg(self, bwPacket):
        r"""!Called on MSG packet"""
        if self._has_sender():
            msg = self.parseWildcards(self.config.get("message_msg", default="{MSG}"))
            self.sender.send_message(msg)

    def teardown(self):
        r"""!Called after alarm"""
        pass

    def onUnload(self):
        r"""!Called by destruction of the plugin"""
        if self._has_sender():
            self.sender.shutdown()
            logger.info("Telegram plugin unloaded")
