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

@file:        bosmon.py
@date:        14.01.2024
@author:      Justin Kurowski | BW2 version: Jens Herrmann
@description: Bosmon Connector Port form BOSWatch2 to BOSWatch 3
"""
import logging
from plugin.pluginBase import PluginBase

# ###################### #
# Custom plugin includes #

import asyncio
from basicauth import encode
import aiohttp

# ###################### #

logging.debug("- %s loaded", __name__)


class BoswatchPlugin(PluginBase):
    r"""!Description of the Plugin"""
    def __init__(self, config):
        r"""!Do not change anything here!"""
        super().__init__(__name__, config)  # you can access the config class on 'self.config'

# Auskommentierte sachen folgen noch! #

    def fms(self, bwPacket):
        r"""!Called on FMS alarm

        @param bwPacket: bwPacket instance
        Remove if not implemented"""
        BM_hostname=self.config.get("hostname")
        BM_port=self.config.get("port")
        BM_user=self.config.get("user")
        BM_passwd=self.config.get("passwd")
        BM_channel=self.config.get("channel")

        get_FMS=bwPacket.get("fms")
        get_status=bwPacket.get("status")
        get_direction=bwPacket.get("direction")
        get_tacticalInfo=bwPacket.get("tacticalInfo")

        self._BosmonRequest_FMS(BM_hostname, BM_port, BM_user, BM_passwd, BM_channel, get_FMS, get_status, get_direction, get_tacticalInfo)

    def pocsag(self, bwPacket):
        r"""!Called on POCSAG alarm

        @param bwPacket: bwPacket instance
        Remove if not implemented"""
        BM_hostname=self.config.get("hostname")
        BM_port=self.config.get("port")
        BM_user=self.config.get("user")
        BM_passwd=self.config.get("passwd")
        BM_channel=self.config.get("channel")

        the_request = 'type=pocsag&address='+bwPacket.get("ric")+'&flags=0&function='+bwPacket.get("subricText")+'&message='+bwPacket.get("message")

        self._post_Request(BM_hostname, BM_port, BM_user, BM_passwd, BM_channel, the_request)


    def zvei(self, bwPacket):
        r"""!Called on ZVEI alarm

        @param bwPacket: bwPacket instance
        Remove if not implemented"""
        BM_hostname=self.config.get("hostname")
        BM_port=self.config.get("port")
        BM_user=self.config.get("user")
        BM_passwd=self.config.get("passwd")
        BM_channel=self.config.get("channel")

        get_zvei_adress=bwPacket.get("tone")

        self._BosmonRequest_Zvei(BM_hostname, BM_port, BM_user, BM_passwd, BM_channel, get_zvei_adress)

    async def _post_Request(self, BM_hostname, BM_port, BM_user, BM_passwd, BM_channel, the_request):
        
        url = BM_hostname+':'+BM_port+'/telegramin/'+BM_channel+'/input.xml'

        payload = the_request
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': encode(BM_user, BM_passwd)
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=payload, headers=headers) as response:
                response_text = await response.text()
                
                asyncio.ensure_future(self._fetch(url, session))

                logging.exception(response_text)

                await response_text

        async def _fetch(self, url, session):
            """Fetches requests

            @param url: url

            @param session: Clientsession instance"""
            async with session.get(url) as response:
                logging.info("{} returned [{}]".format(response.url, response.status))
                return await response.read()