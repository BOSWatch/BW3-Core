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
# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order
from boswatch.utils import paths

if not paths.makeDirIfNotExist(paths.LOG_PATH):
    print("cannot find/create log directory: %s", paths.LOG_PATH)
    exit(1)

import logging.config
logging.config.fileConfig(paths.CONFIG_PATH + "logger_client.ini")
logging.debug("")
logging.debug("######################## NEW LOG ############################")
logging.debug("BOSWatch client has started ...")


logging.debug("Import python modules")
import argparse
logging.debug("- argparse")
import threading
logging.debug("- threading")
import queue
logging.debug("- queue")
import time
logging.debug("- time")

logging.debug("Import BOSWatch modules")
from boswatch.configYaml import ConfigYAML
from boswatch.network.client import TCPClient
from boswatch.network.broadcast import BroadcastClient
from boswatch.processManager import ProcessManager
from boswatch.decoder.decoder import Decoder
from boswatch.utils import header
from boswatch.utils import misc


header.logoToLog()
header.infoToLog()

logging.debug("parse args")
# With -h or --help you get the Args help
parser = argparse.ArgumentParser(prog="bw_client.py",
                                 description="""BOSWatch is a Python Script to receive and
                                 decode german BOS information with rtl_fm and multimon-NG""",
                                 epilog="""More options you can find in the extern client.ini
                                 file in the folder /config""")
parser.add_argument("-c", "--config", help="Name to configuration File", required=True)
parser.add_argument("-t", "--test", help="Start Client with testdata-set")
args = parser.parse_args()

bwConfig = ConfigYAML()
if not bwConfig.loadConfigFile(paths.CONFIG_PATH + args.config):
    logging.error("cannot load config file")
    exit(1)

# ========== CLIENT CODE ==========
try:
    ip = bwConfig.get("server", "ip", default="127.0.0.1")
    port = bwConfig.get("server", "port", default="8080")

    if bwConfig.get("client", "useBroadcast", default=False):
        broadcastClient = BroadcastClient()
        if broadcastClient.getConnInfo():
            ip = broadcastClient.serverIP
            port = broadcastClient.serverPort

    inputQueue = queue.Queue()
    inputThreadRunning = True

    # ========== INPUT CODE ==========
    def handleSDRInput(dataQueue, config):
        sdrProc = ProcessManager("/usr/bin/rtl_fm")
        for freq in config.get("frequencies"):
            sdrProc.addArgument("-f " + freq)
        sdrProc.addArgument("-l 50")  # required fore scanning function
        if not sdrProc.start():
            exit(0)
        # sdrProc.skipLines(20)

        mmProc = ProcessManager("/opt/multimon/multimon-ng", textMode=True)
        mmProc.addArgument("-a FMSFSK -a POCSAG512 -a POCSAG1200 -a POCSAG2400 -a ZVEI1")
        mmProc.addArgument("-f aplha")
        mmProc.addArgument("-t raw -")
        mmProc.setStdin(sdrProc.stdout)
        if not mmProc.start():
            exit(0)
        mmProc.skipLines(5)

        while inputThreadRunning:
            if not sdrProc.isRunning:
                logging.warning("rtl_fm was down - try to restart")
                sdrProc.start()
                # sdrProc.skipLines(20)
            if not mmProc.isRunning:
                logging.warning("multimon was down - try to restart")
                mmProc.start()
                mmProc.skipLines(5)
            if sdrProc.isRunning and mmProc.isRunning:
                line = mmProc.readline()
                if line:
                    dataQueue.put_nowait((line, time.time()))
                    logging.debug("Add data to queue")
                    print(line)
        logging.debug("stoping thread")
        mmProc.stop()
        sdrProc.stop()

    # ========== INPUT CODE ==========

    mmThread = threading.Thread(target=handleSDRInput, name="mmReader", args=(inputQueue, bwConfig.get("inputSource", "sdr")))
    mmThread.daemon = True
    mmThread.start()

    bwClient = TCPClient()
    bwClient.connect(ip, port)
    while 1:

        if not bwClient.isConnected:
            logging.warning("connection to server lost - sleep %d seconds", bwConfig.get("client", "reconnectDelay", default="3"))
            time.sleep(bwConfig.get("client", "reconnectDelay", default="3"))
            bwClient.connect(ip, port)

        elif not inputQueue.empty():
            data = inputQueue.get()
            logging.info("get data from queue (waited %0.3f sec.)", time.time() - data[1])
            logging.debug("%s packet(s) still waiting in queue", inputQueue.qsize())

            bwPacket = Decoder.decode(data[0])
            inputQueue.task_done()

            if bwPacket is None:
                continue

            bwPacket.printInfo()
            misc.addClientDataToPacket(bwPacket, bwConfig)

            for sendCnt in range(bwConfig.get("client", "sendTries", default="3")):
                bwClient.transmit(str(bwPacket))
                if bwClient.receive() == "[ack-]":
                    logging.debug("ack ok")
                    break
                logging.warning("cannot send packet - sleep %d seconds", bwConfig.get("client", "sendDelay", default="3"))
                time.sleep(bwConfig.get("client", "sendDelay", default="3"))

        else:
            time.sleep(0.1)  # reduce cpu load (wait 100ms)
            # in worst case a packet have to wait 100ms until it will be processed


except KeyboardInterrupt:  # pragma: no cover
    logging.warning("Keyboard interrupt")
except SystemExit:  # pragma: no cover
    logging.error("BOSWatch interrupted by an error")
except:  # pragma: no cover
    logging.exception("BOSWatch interrupted by an error")
finally:
    logging.debug("Starting shutdown routine")
    bwClient.disconnect()
    inputThreadRunning = False
    mmThread.join()
    logging.debug("BOSWatch client has stopped ...")
