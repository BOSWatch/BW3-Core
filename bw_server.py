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
from boswatch.utils import paths
if not paths.makeDirIfNotExist(paths.LOG_PATH):
    print("cannot find/create log directory: %s", paths.LOG_PATH)
    exit(1)

try:
    import logging
    import logging.config
    print(paths.CONFIG_PATH + "logger_server.ini")
    logging.config.fileConfig(paths.CONFIG_PATH + "logger_server.ini")
    logging.debug("")
    logging.debug("######################## NEW LOG ############################")
    logging.debug("BOSWatch server has started ...")
except Exception as e:  # pragma: no cover
    print("cannot load logger")
    print(e)
    exit(1)


try:
    logging.debug("Import python modules")
    import argparse
    logging.debug("- argparse")
    # following is temp for testing
    import time
    import sys
    import threading
    import queue

    logging.debug("Import BOSWatch modules")
    from boswatch.config import Config
    from boswatch.network.server import TCPServer
    from boswatch.packet.packet import Packet
    from boswatch.plugin.pluginManager import PluginManager
    from boswatch.descriptor.descriptor import Descriptor
    from boswatch.filter.doubeFilter import DoubleFilter
    from boswatch.utils import header
    from boswatch.network.broadcast import BroadcastClient
    from boswatch.network.broadcast import BroadcastServer
except Exception as e:  # pragma: no cover
    logging.exception("cannot import modules")
    print("cannot import modules")
    print(e)
    exit(1)

#  Test for the broadcast connection info function
server = BroadcastServer()
client = BroadcastClient()
server.start()
print(server.isRunning)
client.getConnInfo()
print(client.serverIP, client.serverPort)
server.stop()
print(server.isRunning)
time.sleep(2)
print(server.isRunning)

try:
    header.logoToLog()
    header.infoToLog()
    header.logoToScreen()

    logging.debug("parse args")
    # With -h or --help you get the Args help
    parser = argparse.ArgumentParser(prog="bw_server.py",
                                     description="""BOSWatch is a Python Script to receive and
                                     decode german BOS information with rtl_fm and multimon-NG""",
                                     epilog="""More options you can find in the extern client.ini
                                     file in the folder /config""")
    parser.add_argument("-c", "--config", help="Name to configuration File", required=True)
    args = parser.parse_args()

    bwConfig = Config()
    if bwConfig.loadConfigFile(paths.CONFIG_PATH + args.config, "serverConfig") is False:
        logging.exception("cannot load config file")
        print("cannot load config file")
        exit(1)  # without config cannot run

    bwPluginManager = PluginManager()
    bwPluginManager.searchPluginDir()
    bwPluginManager.importAllPlugins()
    bwPluginManager.loadAllPlugins()

    bwDescriptor = Descriptor()
    if bwConfig.getBool("Description", "fms"):
        bwDescriptor.loadDescription("fms")
    if bwConfig.getBool("Description", "pocsag"):
        bwDescriptor.loadDescription("pocsag")
    if bwConfig.getBool("Description", "zvei"):
        bwDescriptor.loadDescription("zvei")

    bwDoubleFilter = DoubleFilter()

    serverPaused = False  # flag to pause alarming of server
    serverStop = False  # flag to stop the whole server application

    # server flags test code
    # ----------------------
    # import threading
    # def eins():
    #     global serverPaused
    #     serverPaused = True
    # def zwei():
    #     global serverPaused
    #     serverPaused = False
    def drei():
        global serverStop
        serverStop = True
    #
    # t1 = threading.Timer(1, eins)
    # t2 = threading.Timer(5, zwei)
    # t3 = threading.Timer(15, drei)
    # t1.start()
    # t2.start()
    # t3.start()

    incomingQueue = queue.Queue()
    bwServer = TCPServer(incomingQueue)
    if bwServer.start():

        while 1:
            if serverPaused:
                logging.warning("Server pause flag received ...")
                logging.debug("But all received packages will be cached!")
                packetsOld = 0
                while serverPaused is True:
                    time.sleep(0.2)  # reduce cpu load (run all 200ms)
                    packetsNew = incomingQueue.qsize()
                    if packetsNew is not packetsOld:
                        logging.debug("%s packet(s) waiting in queue", packetsNew)
                        packetsOld = packetsNew
                logging.warning("Server resumed ...")

            if serverStop:
                logging.warning("Server stop flag received ...")
                break

            if incomingQueue.empty():  # pause only when no data
                time.sleep(0.1)  # reduce cpu load (run all 100ms)

            data = incomingQueue.get()
            if data is not None:
                logging.info("get data from %s (waited in queue %0.3f sec.)", data[0], time.time() - data[2])
                logging.debug("%s packet(s) waiting in queue", incomingQueue.qsize())
                bwPacket = Packet((data[1]))

                if not bwDoubleFilter.filter(bwPacket):
                    continue

                bwPacket.set("clientIP", data[0])
                bwPacket.addServerData()

                if bwConfig.getBool("Description", bwPacket.get("mode")):
                    bwDescriptor.addDescriptions(bwPacket)

                bwPluginManager.runAllPlugins(bwPacket)
                # print(bwPacket.get("clientVersion")["major"])
                incomingQueue.task_done()

except KeyboardInterrupt:  # pragma: no cover
    logging.warning("Keyboard interrupt")
except SystemExit:  # pragma: no cover
    logging.error("BOSWatch interrupted by an error")
except:  # pragma: no cover
    logging.exception("BOSWatch interrupted by an error")
finally:  # pragma: no cover
    # try-except-blocks are necessary because there is a change that the vars
    # bwServer or bwPluginManager are not defined in case of an early error
    try:
        bwServer.stop()
    except:  # pragma: no cover
        pass
    try:
        bwPluginManager.unloadAllPlugins()
    except:  # pragma: no cover
        pass
    logging.debug("BOSWatch has ended ...")
