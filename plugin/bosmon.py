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

import requests
from basicauth import encode

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

        get_ric=bwPacket.get("ric")
        get_subric=bwPacket.get("subricText")
        get_message=bwPacket.get("message")

        self._BosmonRequest_Poc(BM_hostname, BM_port, BM_user, BM_passwd, BM_channel, get_ric, get_subric, get_message)

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

    def _BosmonRequest_Poc(self, BM_hostname, BM_port, BM_user, BM_passwd, BM_channel, get_ric, get_subric, get_message):
        
        url = 'http://'+BM_hostname+':'+BM_port+'/telegramin/'+BM_channel+'/input.xml'

        payload = 'type=pocsag&address='+get_ric+'&flags=0&function='+get_subric+'&message='+get_message
        headers = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Authorization': encode(BM_user, BM_passwd)
                }

        requests.request("POST", url, headers=headers, data=payload)

    def _BosmonRequest_FMS(self, BM_hostname, BM_port, BM_user, BM_passwd, BM_channel, get_FMS, get_status, get_direction, get_tacticalInfo):
                                                        
            
            # BosMon-Telegramin expected assembly group, direction and tsi in one field
            # structure (binary as hex in base10):
            #     Byte 1: assembly group; Byte 2: Direction; Byte 3+4: tactic short info
            info = 0
            # assembly group:
            info = info + 1          # + b0001 (Assumption: is in every time 1 (no output from multimon-ng))
            # direction:
            if get_direction == "1":
                info = info + 2      # + b0010
                # tsi:
            if "IV" in get_tacticalInfo:
                info = info + 12     # + b1100
            elif "III" in get_tacticalInfo:
                info = info + 8      # + b1000
            elif "II" in get_tacticalInfo:
                info = info + 4      # + b0100
                # "I" is nothing to do     + b0000
                
            
            url = 'http://'+BM_hostname+':'+BM_port+'/telegramin/'+BM_channel+'/input.xml'
    
            payload = 'type=fms&address='+get_FMS+'&flags=0&status='+get_status+'&info='+info

            headers = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Authorization': encode(BM_user, BM_passwd)
                }
            
            requests.request("POST", url, headers=headers, data=payload)
                
            
    def _BosmonRequest_Zvei(self, BM_hostname, BM_port, BM_user, BM_passwd, BM_channel, get_zvei_adress):
         
        url = 'http://'+BM_hostname+':'+BM_port+'/telegramin/'+BM_channel+'/input.xml'

        payload = 'type=pocsag&address='+get_zvei_adress+'&flags=0'
        headers = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Authorization': encode(BM_user, BM_passwd)
                }

        requests.request("POST", url, headers=headers, data=payload)