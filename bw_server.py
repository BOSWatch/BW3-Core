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

@file:        bw_server.py
@date:        09.12.2017
@author:      Bastian Schroll
@description: BOSWatch server application
"""
# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order

import sys
major_version = sys.version_info.major
assert major_version >= 3, "please use python3 to run BosWatch 3"

from boswatch.utils import paths

if not paths.makeDirIfNotExist(paths.LOG_PATH):
    print("cannot find/create log directory: %s", paths.LOG_PATH)
    exit(1)

import logging.config
logging.config.fileConfig(paths.CONFIG_PATH + "logger_server.ini")
logging.debug("")
logging.debug("######################## NEW LOG ############################")
logging.debug("BOSWatch server has started ...")


logging.debug("Import python modules")
import argparse
logging.debug("- argparse")
import queue
logging.debug("- queue")
import time
logging.debug("- time")

logging.debug("Import BOSWatch modules")
from boswatch.configYaml import ConfigYAML
from boswatch.network.server import TCPServer
from boswatch.packet import Packet
from boswatch.utils import header
from boswatch.network.broadcast import BroadcastServer
from boswatch.router.routerManager import RouterManager
from boswatch.utils import misc

header.logoToLog()
header.infoToLog()

# With -h or --help you get the Args help
parser = argparse.ArgumentParser(prog="bw_server.py",
                                 description="""BOSWatch is a Python Script to receive and
                                 decode german BOS information with rtl_fm and multimon-NG""",
                                 epilog="""More options you can find in the extern client.ini
                                 file in the folder /config""")
parser.add_argument("-c", "--config", help="Name to configuration File", required=True)
args = parser.parse_args()


bwConfig = ConfigYAML()
if not bwConfig.loadConfigFile(paths.CONFIG_PATH + args.config):
    logging.fatal("cannot load config file")
    exit(1)

# ############################# begin server system
bwRoutMan = None
bwServer = None
bcServer = None

try:
    bwRoutMan = RouterManager()
    if not bwRoutMan.buildRouters(bwConfig):
        logging.fatal("Error while building routers")
        exit(1)

    bcServer = BroadcastServer()
    if bwConfig.get("server", "useBroadcast", default=False):
        bcServer.start()

    incomingQueue = queue.Queue()
    bwServer = TCPServer(incomingQueue)
    if bwServer.start():

        while 1:
            if incomingQueue.empty():  # pause only when no data
                time.sleep(0.1)  # reduce cpu load (wait 100ms)
                # in worst case a packet have to wait 100ms until it will be processed

            else:
                data = incomingQueue.get()

                logging.info("get data from %s (waited in queue %0.3f sec.)", data[0], time.time() - data[2])
                logging.debug("%s packet(s) still waiting in queue", incomingQueue.qsize())
                bwPacket = Packet((data[1]))

                bwPacket.set("clientIP", data[0])
                misc.addServerDataToPacket(bwPacket, bwConfig)

                logging.debug("[ ---   ALARM   --- ]")
                bwRoutMan.runRouters(bwConfig.get("alarmRouter"), bwPacket)
                logging.debug("[ --- END ALARM --- ]")

                incomingQueue.task_done()

except KeyboardInterrupt:  # pragma: no cover
    logging.warning("Keyboard interrupt")
except SystemExit:  # pragma: no cover
    logging.error("BOSWatch interrupted by an error")
except:  # pragma: no cover
    logging.exception("BOSWatch interrupted by an error")
finally:
    logging.debug("Starting shutdown routine")
    if bwRoutMan:
        bwRoutMan.cleanup()
    if bwServer:
        bwServer.stop()
    if bcServer:
        bcServer.stop()
    logging.debug("BOSWatch server has stopped ...")
