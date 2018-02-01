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

# from boswatch.module import file

logging.debug("- %s loaded", __name__)

# todo insert all wildcards and delete testcode under the function


def replaceWildcards(message): #, bwPacket):
    _wildcards = {
        # formatting wildcards
        "%BR%": "\r\n",
        "%LPAR%": "(",
        "%RPAR%": ")",

        # boswatch wildcards
        "%MODE%": "",# bwPacket.getField("mode"),
        "%FREQ% ": "",# bwPacket.getField("frequency")

        # fms wildcards
        # pocsag wildcards
        # zvei wildcards
    }
    message.replace("nett", "test")

    for wildcard in _wildcards:
        try:
            message = message.replace(wildcard, _wildcards[wildcard])
        except:
            logging.exception("error in wildcard replacement")

    return message


ttext = "das ist ein test %BR% der echt gut %TEST% ist weil %LPAR% er es ust."
print(ttext)
print(replaceWildcards(ttext))
