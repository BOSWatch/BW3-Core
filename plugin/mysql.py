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

@file:        mysql.py
@date:        15.02.2021
@author:      Jan Speller
@description: Mysql Plugin
"""
import logging
from plugin.pluginBase import PluginBase

# ###################### #
# Custom plugin includes #
import mysql.connector
from datetime import datetime

# ###################### #

logging.debug("- %s loaded", __name__)


class BoswatchPlugin(PluginBase):
    """!Description of the Plugin"""

    def __init__(self, config):
        """!Do not change anything here!"""
        super().__init__(__name__, config)  # you can access the config class on 'self.config'

    def onLoad(self):
        """!Called by import of the plugin
        Remove if not implemented"""
        self.sqlInserts = {
            "pocsag": "INSERT INTO boswatch (packetTimestamp, packetMode, pocsag_ric, pocsag_subric, pocsag_subricText, pocsag_message, pocsag_bitrate, serverName, serverVersion, serverBuildDate, serverBranch, clientName, clientIP, clientVersion, clientBuildDate, clientBranch, inputSource, frequency) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            "zvei": "INSERT INTO boswatch (packetTimestamp, packetMode, zvei_tone, serverName, serverVersion, serverBuildDate, serverBranch, clientName, clientIP, clientVersion, clientBuildDate, clientBranch, inputSource, frequency) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            "fms": "INSERT INTO boswatch (packetTimestamp, packetMode, fms_fms, fms_service, fms_country, fms_location, fms_vehicle, fms_status, fms_direction, fms_directionText, fms_tacticalInfo, serverName, serverVersion, serverBuildDate, serverBranch, clientName, clientIP, clientVersion, clientBuildDate, clientBranch, inputSource, frequency) VALUE (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            "msg": "INSERT INTO boswatch (packetTimestamp, packetMode, serverName, serverVersion, serverBuildDate, serverBranch, clientName, clientIP, clientVersion, clientBuildDate, clientBranch, inputSource, frequency) VALUE (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        }

        self.connection = mysql.connector.connect(
            host=self.config.get("host"),
            user=self.config.get("user"),
            password=self.config.get("password"),
            database=self.config.get("database"),
        )

        self.cursor = self.connection.cursor()
        self.cursor.execute("SHOW TABLES LIKE 'boswatch'")

        if self.cursor.fetchone() is None:
            with open('init_db.sql') as f:
                for stmnt in f.read().split(';'):
                    self.cursor.execute(stmnt)
                    self.connection.commit()

        self.cursor.close()

    def setup(self):
        """!Called before alarm
        Remove if not implemented"""
        try:
            self.connection.ping(reconnect=True, attempts=3, delay=2)
        except mysql.connector.Error:
            logging.warning("Connection was down, trying to reconnect...")
            self.onLoad()

        self.cursor = self.connection.cursor()

    def fms(self, bwPacket):
        """!Called on FMS alarm

        @param bwPacket: bwPacket instance
        Remove if not implemented"""
        val = (
            datetime.fromtimestamp(float(bwPacket.get("timestamp"))),
            bwPacket.get("mode"),
            bwPacket.get("fms"),
            bwPacket.get("service"),
            bwPacket.get("country"),
            bwPacket.get("location"),
            bwPacket.get("vehicle"),
            bwPacket.get("status"),
            bwPacket.get("direction"),
            bwPacket.get("directionText"),
            bwPacket.get("tacticalInfo"),
            bwPacket.get("serverName"),
            bwPacket.get("serverVersion"),
            bwPacket.get("serverBuildDate"),
            bwPacket.get("serverBranch"),
            bwPacket.get("clientName"),
            bwPacket.get("clientIP"),
            bwPacket.get("clientVersion"),
            bwPacket.get("clientBuildDate"),
            bwPacket.get("clientBranch"),
            bwPacket.get("inputSource"),
            bwPacket.get("frequency")
        )
        self.cursor.execute(self.sqlInserts.get("fms"), val)

    def pocsag(self, bwPacket):
        """!Called on POCSAG alarm

        @param bwPacket: bwPacket instance
        Remove if not implemented"""
        val = (
            datetime.fromtimestamp(float(bwPacket.get("timestamp"))),
            bwPacket.get("mode"),
            bwPacket.get("ric"),
            bwPacket.get("subric"),
            bwPacket.get("subricText"),
            bwPacket.get("message"),
            bwPacket.get("bitrate"),
            bwPacket.get("serverName"),
            bwPacket.get("serverVersion"),
            bwPacket.get("serverBuildDate"),
            bwPacket.get("serverBranch"),
            bwPacket.get("clientName"),
            bwPacket.get("clientIP"),
            bwPacket.get("clientVersion"),
            bwPacket.get("clientBuildDate"),
            bwPacket.get("clientBranch"),
            bwPacket.get("inputSource"),
            bwPacket.get("frequency")
        )
        self.cursor.execute(self.sqlInserts.get("pocsag"), val)

    def zvei(self, bwPacket):
        """!Called on ZVEI alarm

        @param bwPacket: bwPacket instance
        Remove if not implemented"""
        val = (
            datetime.fromtimestamp(float(bwPacket.get("timestamp"))),
            bwPacket.get("mode"),
            bwPacket.get("tone"),
            bwPacket.get("serverName"),
            bwPacket.get("serverVersion"),
            bwPacket.get("serverBuildDate"),
            bwPacket.get("serverBranch"),
            bwPacket.get("clientName"),
            bwPacket.get("clientIP"),
            bwPacket.get("clientVersion"),
            bwPacket.get("clientBuildDate"),
            bwPacket.get("clientBranch"),
            bwPacket.get("inputSource"),
            bwPacket.get("frequency")
        )
        self.cursor.execute(self.sqlInserts.get("pocsag"), val)

    def msg(self, bwPacket):
        """!Called on MSG packet

        @param bwPacket: bwPacket instance
        Remove if not implemented"""
        val = (
            datetime.fromtimestamp(float(bwPacket.get("timestamp"))),
            bwPacket.get("mode"),
            bwPacket.get("serverName"),
            bwPacket.get("serverVersion"),
            bwPacket.get("serverBuildDate"),
            bwPacket.get("serverBranch"),
            bwPacket.get("clientName"),
            bwPacket.get("clientIP"),
            bwPacket.get("clientVersion"),
            bwPacket.get("clientBuildDate"),
            bwPacket.get("clientBranch"),
            bwPacket.get("inputSource"),
            bwPacket.get("frequency")
        )
        self.cursor.execute(self.sqlInserts.get("msg"), val)

    def teardown(self):
        """!Called after alarm
        Remove if not implemented"""
        self.connection.commit()
        self.cursor.close()

    def onUnload(self):
        """!Called by destruction of the plugin
        Remove if not implemented"""
        self.connection.close()
