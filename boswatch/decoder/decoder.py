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

@file:        decoder.py
@date:        06.01.2018
@author:      Bastian Schroll
@description: Some utils for the decoding
"""
import logging

from boswatch.decoder.fms import Fms
from boswatch.decoder.pocsag import Pocsag
from boswatch.decoder.zvei import Zvei

logging.debug("- %s loaded", __name__)


def getDecoder(data):
    """!Choose the right decoder and return the new decoder object

    @param data: data to decode
    @return Decoder object"""
    logging.debug("search decoder")
    if "FMS" in data:
        return Fms()
    elif "POCSAG" in data:
        return Pocsag()
    elif "ZVEI" in data:
        return Zvei()
    else:
        logging.debug("no decoder found for: %s", data)
        return DummyDecoder()


class DummyDecoder:
    """!This dummy decoder class is needed because in case of
    an getDecoder() with false data, we must return a decoder
    object with an decode() method to prevent an error"""
    def __init__(self):
        """!Do nothing"""
        pass

    @staticmethod
    def decode(data):
        """!Dummy decode() method

        @param data: data to decode
        @return ALWAYS None"""
        return None
