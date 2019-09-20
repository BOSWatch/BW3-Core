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

from boswatch.decoder.fmsdecoder import FmsDecoder
from boswatch.decoder.pocsagdecoder import PocsagDecoder
from boswatch.decoder.zveidecoder import ZveiDecoder

logging.debug("- %s loaded", __name__)


class Decoder:

    @staticmethod
    def decode(data):
        """!Choose the right decoder and return a bwPacket instance

        @param data: data to decode
        @return bwPacket instance"""
        logging.debug("search decoder")
        data = str(data)
        if "FMS" in data:
            return FmsDecoder.decode(data)
        elif "POCSAG" in data:
            return PocsagDecoder.decode(data)
        elif "ZVEI" in data:
            return ZveiDecoder.decode(data)
        else:
            logging.error("no decoder found for: %s", data)
            return None
