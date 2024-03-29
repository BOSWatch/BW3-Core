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

@file:        decoder.py
@date:        06.01.2018
@author:      Bastian Schroll
@description: Some utils for the decoding
"""
import logging

from boswatch.decoder.fmsDecoder import FmsDecoder
from boswatch.decoder.pocsagDecoder import PocsagDecoder
from boswatch.decoder.zveiDecoder import ZveiDecoder

logging.debug("- %s loaded", __name__)


class Decoder:

    @staticmethod
    def decode(data):
        r"""!Choose the right decoder and return a bwPacket instance

        @param data: data to decode
        @return bwPacket instance"""
        data = str(data)
        if "FMS" in data:
            return FmsDecoder.decode(data)
        elif "POCSAG" in data:
            return PocsagDecoder.decode(data)
        elif "ZVEI" in data:
            return ZveiDecoder.decode(data)
        else:
            logging.warning("no decoder found for: %s", data)
            return None
