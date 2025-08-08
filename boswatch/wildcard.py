#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""!
    ____  ____  ______        __      __      __      _____
   / __ )/ __ \/ ___/ |      / /___ _/ /______/ /_     |__  /
  / __  / / / /\__ \| | /| / / __ `/ __/ ___/ __ \     /_ <
 / /_/ / /_/ /___/ /| |/ |/ / /_/ / /_/ /__/ / / /   ___/ /
/_____/\____//____/ |__/|__/\__,_/\__/\___/_/ /_/   /____/
                   German BOS Information Script
                         by Bastian Schroll

@file:       wildcard.py
@date:       23.07.2025
@author:     Bastian Schroll
@description: Functions to replace wildcards in stings
"""
import logging
import time

logging.debug("- %s loaded", __name__)

_additionalWildcards = {}


def registerWildcard(wildcard, bwPacketField):
    r"""!Register a new additional wildcard

    @param wildcard: New wildcard string with format: '{WILDCARD}'
    @param bwPacketField: Field of the bwPacket which is used for wildcard replacement"""
    if wildcard in _additionalWildcards:
        logging.error("wildcard always registered: %s", wildcard)
        return
    logging.debug("register new wildcard %s for field: %s", wildcard, bwPacketField)
    _additionalWildcards[wildcard] = bwPacketField


def replaceWildcards(message, bwPacket):
    r"""!Replace the wildcards in a given message

    @param message: Message in which wildcards should be replaced
    @param bwPacket: bwPacket instance with the replacement information
    @return Input message with the replaced wildcards"""

    # Start with wildcards that are always available
    _wildcards = {
        # formatting wildcards
        # todo check if br and par are needed - if not also change config
        "{BR}": "\r\n",
        "{LPAR}": "(",
        "{RPAR}": ")",
        "{TIME}": time.strftime("%d.%m.%Y %H:%M:%S"),

        # info wildcards
        # server
        "{SNAME}": bwPacket.get("serverName"),
        "{SVERS}": bwPacket.get("serverVersion"),
        "{SDATE}": bwPacket.get("serverBuildDate"),
        "{SBRCH}": bwPacket.get("serverBranch"),

        # client
        "{CNAME}": bwPacket.get("clientName"),
        "{CIP}": bwPacket.get("clientIP"),
        "{CVERS}": bwPacket.get("clientVersion"),
        "{CDATE}": bwPacket.get("clientBuildDate"),
        "{CBRCH}": bwPacket.get("clientBranch"),

        # boswatch wildcards
        "{INSRC}": bwPacket.get("inputSource"),
        "{TIMES}": bwPacket.get("timestamp"),
        "{FREQ}": bwPacket.get("frequency"),
        "{MODE}": bwPacket.get("mode"),
    }

    # Get the packet mode to add specific wildcards
    mode = bwPacket.get("mode")

    # fms wildcards
    if mode == "fms":
        fms_wildcards = {
            "{FMS}": bwPacket.get("fms"),
            "{SERV}": bwPacket.get("service"),
            "{COUNT}": bwPacket.get("country"),
            "{LOC}": bwPacket.get("location"),
            "{VEHC}": bwPacket.get("vehicle"),
            "{STAT}": bwPacket.get("status"),
            "{DIR}": bwPacket.get("direction"),
            "{DIRT}": bwPacket.get("directionText"),
            "{TACI}": bwPacket.get("tacticalInfo"),
        }
        _wildcards.update(fms_wildcards)

    # pocsag wildcards
    elif mode == "pocsag":
        pocsag_wildcards = {
            "{BIT}": bwPacket.get("bitrate"),
            "{RIC}": bwPacket.get("ric"),
            "{SRIC}": bwPacket.get("subric"),
            "{SRICT}": bwPacket.get("subricText"),
            "{MSG}": bwPacket.get("message"),
        }
        _wildcards.update(pocsag_wildcards)

    # zvei wildcards
    elif mode == "zvei":
        zvei_wildcards = {
            "{TONE}": bwPacket.get("tone"),
        }
        _wildcards.update(zvei_wildcards)

    # msg wildcards
    elif mode == "msg":
        msg_wildcards = {
            "{MSG}": bwPacket.get("message"),
        }
        _wildcards.update(msg_wildcards)

    # Now, replace all collected wildcards
    for wildcard, field in _wildcards.items():
        # Only replace if the field was found in the packet (is not None)
        if field is not None:
            message = message.replace(wildcard, field)

    # Handle additional, dynamically registered wildcards
    for wildcard, fieldName in _additionalWildcards.items():
        field = bwPacket.get(fieldName)
        if field is not None:
            message = message.replace(wildcard, field)

    return message
