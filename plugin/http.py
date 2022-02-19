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

@file:        http.py
@date:        23.02.2020
@author:      Jan Speller
@description: Http Plugin
"""
import logging
from plugin.pluginBase import PluginBase

# ###################### #
# Custom plugin includes #
import asyncio
from aiohttp import ClientSession
# ###################### #

logging.debug("- %s loaded", __name__)


class BoswatchPlugin(PluginBase):
    """!Description of the Plugin"""
    def __init__(self, config):
        """!Do not change anything here!"""
        super().__init__(__name__, config)  # you can access the config class on 'self.config'

    def fms(self, bwPacket):
        """!Called on FMS alarm

        @param bwPacket: bwPacket instance
        Remove if not implemented"""
        urls = self.config.get("fms")
        self._makeRequests(urls)

    def pocsag(self, bwPacket):
        """!Called on POCSAG alarm

        @param bwPacket: bwPacket instance
        Remove if not implemented"""
        urls = self.config.get("pocsag")
        self._makeRequests(urls)

    def zvei(self, bwPacket):
        """!Called on ZVEI alarm

        @param bwPacket: bwPacket instance
        Remove if not implemented"""
        urls = self.config.get("zvei")
        self._makeRequests(urls)

    def msg(self, bwPacket):
        """!Called on MSG packet

        @param bwPacket: bwPacket instance
        Remove if not implemented"""
        urls = self.config.get("msg")
        self._makeRequests(urls)

    def _makeRequests(self, urls):
        """Parses wildcard urls and handles asynchronus requests

        @param urls: array of urls"""
        urls = [self.parseWildcards(url) for url in urls]

        loop = asyncio.get_event_loop()

        future = asyncio.ensure_future(self.asyncRequests(urls))
        loop.run_until_complete(future)

    async def _asyncRequests(self, urls):
        """Handles asynchronus requests

        @param urls: array of urls to send requests to"""
        tasks = []

        async with ClientSession() as session:
            for url in urls:
                task = asyncio.ensure_future(self._fetch(url, session))
                tasks.append(task)

            responses = asyncio.gather(*tasks)
            await responses

    async def _fetch(self, url, session):
        """Fetches requests

        @param url: url

        @param session: Clientsession instance"""
        async with session.get(url) as response:
            logging.info("{} returned [{}]".format(response.url, response.status))
            return await response.read()
