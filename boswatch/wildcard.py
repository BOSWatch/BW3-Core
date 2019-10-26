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
@description: Functions to replace wildcards in stings
"""
import logging
import time

logging.debug("- %s loaded", __name__)

# todo check function and document + write an test

_additionalWildcards = {}


def registerWildcard(wildcard, bwPacketField):
    if wildcard in _additionalWildcards:
        logging.error("wildcard always registered: %s", wildcard)
        return
    logging.debug("register new wildcard %s for field: %s", wildcard, bwPacketField)
    _additionalWildcards[wildcard] = bwPacketField


def replaceWildcards(message, bwPacket):
    _wildcards = {
        # formatting wildcards
        # todo check if br and par are needed - if not also change config
        "{BR}": "\r\n",
        "{LPAR}": "(",
        "{RPAR}": ")",
        "{TIME}": time.strftime("%d.%m.%Y %H:%M:%S"),

        # info wildcards
        # server
        "{SNAME}": bwPacket.getField("serverName"),
        "{SVERS}": bwPacket.getField("serverVersion"),
        "{SDATE}": bwPacket.getField("serverBuildDate"),
        "{SBRCH}": bwPacket.getField("serverBranch"),

        # client
        "{CNAME}": bwPacket.getField("clientName"),
        "{CIP}": bwPacket.getField("clientIP"),
        "{CVERS}": bwPacket.getField("clientVersion"),
        "{CDATE}": bwPacket.getField("clientBuildDate"),
        "{CBRCH}": bwPacket.getField("clientBranch"),

        # boswatch wildcards
        "{INSRC}": bwPacket.getField("mode"),
        "{TIMES}": bwPacket.getField("mode"),
        "{FREQ}": bwPacket.getField("frequency"),
        "{MODE}": bwPacket.getField("mode"),

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
    for wildcard, field in _wildcards.items():
        message = message.replace(wildcard, field)

    for wildcard, field in _additionalWildcards.items():
        message = message.replace(wildcard, bwPacket.getField(field))

    return message
