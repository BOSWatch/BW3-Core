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

@file:        wildcard.py
@date:        15.01.2018
@author:      Bastian Schroll
@description: Little Helper to replace wildcards in stings
@todo not completed yet
"""
import logging
import time

# from boswatch.module import file

logging.debug("- %s loaded", __name__)

# todo check function and document + write an test


def replaceWildcards(message, bwPacket):
    _wildcards = {
        # formatting wildcards
        "{BR}": "\r\n",
        "{LPAR}": "(",
        "{RPAR}": ")",

        # info wildcards
        "{SNAME}": bwPacket.getField("serverName"),
        "{SVERS}": bwPacket.getField("serverVersion"),
        "{SDATE}": bwPacket.getField("serverBuildDate"),
        "{SBRCH}": bwPacket.getField("serverBranch"),
        "{CNAME}": bwPacket.getField("clientName"),
        "{CIP}":   bwPacket.getField("clientIP"),
        "{CVERS}": bwPacket.getField("clientVersion"),
        "{CDATE}": bwPacket.getField("clientBuildDate"),
        "{CBRCH}": bwPacket.getField("clientBranch"),

        # boswatch wildcards
        "{MODE}": bwPacket.getField("mode"),
        "{FREQ}": bwPacket.getField("frequency"),
        "{DESCS}": bwPacket.getField("descriptionShort"),
        "{DESCL}": bwPacket.getField("descriptionLong"),
        "{INSRC}": bwPacket.getField("mode"),
        "{TIME}": time.time(),
        "{TIMES}": bwPacket.getField("mode"),

        # fms wildcards
        "{FMS}": bwPacket.getField("fms"),
        "{SERV}": bwPacket.getField("service"),
        "{COUNT}": bwPacket.getField("country"),
        "{LOC}": bwPacket.getField("location"),
        "{VEHC}": bwPacket.getField("vehicle"),
        "{STAT}": bwPacket.getField("status"),
        "{DIR}": bwPacket.getField("direction"),
        "{DIRT}": bwPacket.getField("dirextionText"),
        "{TACI}": bwPacket.getField("tacticalInfo"),

        # pocsag wildcards
        "{BIT}": bwPacket.getField("bitrate"),
        "{RIC}": bwPacket.getField("ric"),
        "{SRIC}": bwPacket.getField("subric"),
        "{SRICT}": bwPacket.getField("subricText"),
        "{MSG}": bwPacket.getField("message"),

        # zvei wildcards
        "{TONE}": bwPacket.getField("tone"),

        # message for MSG packet is done in poc
    }
    for wildcard in _wildcards:
        try:
            message = message.replace(wildcard, _wildcards[wildcard])
        except:
            logging.exception("error in wildcard replacement")

    return message
