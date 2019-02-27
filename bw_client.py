#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    ____  ____  ______       __      __       __       _____
   / __ )/ __ \/ ___/ |     / /___ _/ /______/ /_     |__  /
  / __  / / / /\__ \| | /| / / __ `/ __/ ___/ __ \     /_ <
 / /_/ / /_/ /___/ /| |/ |/ / /_/ / /_/ /__/ / / /   ___/ /
/_____/\____//____/ |__/|__/\__,_/\__/\___/_/ /_/   /____/
                German BOS Information Script
                     by Bastian Schroll

@file:        bw_client.py
@date:        09.12.2017
@author:      Bastian Schroll
@description: BOSWatch client application
"""
from boswatch.utils import paths

if not paths.makeDirIfNotExist(paths.LOG_PATH):
    print("cannot find/create log directory: %s", paths.LOG_PATH)
    exit(1)

try:
    import logging
    import logging.config

    logging.config.fileConfig(paths.CONFIG_PATH + "logger_client.ini")
    logging.debug("")
    logging.debug("######################## NEW LOG ############################")
    logging.debug("BOSWatch client has started ...")
except Exception as e:  # pragma: no cover
    print("cannot load logger")
    print(e)
    exit(1)

try:
    logging.debug("Import python modules")
    import argparse
    logging.debug("- argparse")
    import subprocess
    logging.debug("- subprocess")
    # following is temp for testing
    import time

    logging.debug("Import BOSWatch modules")
    from boswatch import configYaml
    from boswatch.network.client import TCPClient
    from boswatch.network.broadcast import BroadcastClient
    from boswatch.decoder.decoder import Decoder
    from boswatch.utils import header
except Exception as e:  # pragma: no cover
    logging.exception("cannot import modules")
    print("cannot import modules")
    print(e)
    exit(1)

try:
    header.logoToLog()
    header.infoToLog()
    header.logoToScreen()

    logging.debug("parse args")
    # With -h or --help you get the Args help
    parser = argparse.ArgumentParser(prog="bw_client.py",
                                     description="""BOSWatch is a Python Script to receive and
                                     decode german BOS information with rtl_fm and multimon-NG""",
                                     epilog="""More options you can find in the extern client.ini
                                     file in the folder /config""")
    parser.add_argument("-c", "--config", help="Name to configuration File", required=True)
    parser.add_argument("-t", "--test", help="Client will send some testdata", action="store_true")  # todo implement testmode
    args = parser.parse_args()

    bwConfig = configYaml.loadConfigFile(paths.CONFIG_PATH + args.config, "clientConfig")
    if bwConfig is None:
        logging.error("cannot load config file")

except Exception as e:  # pragma: no cover
    logging.exception("error occurred")
    exit(1)


# ############################# begin client system
try:

    if bwConfig["client"]["useBroadcast"]:
        broadcastClient = BroadcastClient()
        if broadcastClient.getConnInfo():
            ip = broadcastClient.serverIP
            port = broadcastClient.serverPort
    else:
        ip = bwConfig["server"]["ip"]
        port = bwConfig["server"]["port"]

    bwClient = TCPClient()
    if bwClient.connect(ip, port):

        while 1:
            for i in range(0, 5):
                time.sleep(1)
                print("Alarm Nr #" + str(i))

                data = "ZVEI1: 12345"
                bwPacket = Decoder.decode(data)

                if bwPacket:
                    bwPacket.printInfo()
                    bwPacket.addClientData()
                    bwClient.transmit(str(bwPacket))

                    # todo should we do this in an thread, to not block receiving ??? but then we should use transmit() and receive() with Lock()
                    failedTransmits = 0
                    while not bwClient.receive() == "[ack]":  # wait for ack or timeout
                        if failedTransmits >= 3:
                            logging.error("cannot transmit after 3 retires")
                            break
                        failedTransmits += 1
                        logging.warning("attempt %d to resend packet", failedTransmits)
                        bwClient.transmit(str(bwPacket))  # try to resend

                    logging.debug("ack ok")

            bwClient.disconnect()
            break
# test for server ####################################

except KeyboardInterrupt:  # pragma: no cover
    logging.warning("Keyboard interrupt")
except SystemExit:  # pragma: no cover
    logging.error("BOSWatch interrupted by an error")
except:  # pragma: no cover
    logging.exception("BOSWatch interrupted by an error")
finally:  # pragma: no cover
    logging.debug("BOSWatch has ended ...")
