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

@file:        misc.py
@date:        11.03.2019
@author:      Bastian Schroll
@description: Some misc functions
"""
import logging
from boswatch.utils import version

logging.debug("- %s loaded", __name__)


def addClientDataToPacket(bwPacket, config):
    """!Add the client information to the decoded data

    This function adds the following data to the bwPacket:
    - clientName
    - clientVersion
    - clientBuildDate
    - clientBranch
    - inputSource
    - frequency"""
    logging.debug("add client data to bwPacket")
    bwPacket.set("clientName", config.get("client", "name"))
    bwPacket.set("clientVersion", version.client)
    bwPacket.set("clientBuildDate", version.date)
    bwPacket.set("clientBranch", version.branch)
    bwPacket.set("inputSource", config.get("client", "inputSource"))
    bwPacket.set("frequency", config.get("inputSource", "sdr", "frequency"))


def addServerDataToPacket(bwPacket, config):
    """!Add the server information to the decoded data

    This function adds the following data to the bwPacket:
    - serverName
    - serverVersion
    - serverBuildDate
    - serverBranch"""
    logging.debug("add server data to bwPacket")
    bwPacket.set("serverName", config.get("server", "name"))
    bwPacket.set("serverVersion", version.server)
    bwPacket.set("serverBuildDate", version.date)
    bwPacket.set("serverBranch", version.branch)
