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

@file:        broadcast.py
@date:        21.09.2018
@author:      Bastian Schroll
@description: UDP broadcast server and client class
"""
import logging
import socket
import threading

logging.debug("- %s loaded", __name__)


class BroadcastClient:

    def __init__(self, port=5000):
        self._broadcastPort = port

        self._serverIP = ""
        self._serverPort = 0

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self._socket.settimeout(3)

    def sendBroadcast(self):
        while True:
            try:
                logging.debug("send magic <BW3-Request> as broadcast")
                self._socket.sendto("<BW3-Request>".encode(), ('255.255.255.255', self._broadcastPort))
                payload, address = self._socket.recvfrom(1024)
                payload = str(payload, "UTF-8")

                if payload.startswith("<BW3-Result>"):
                    logging.debug("received magic <BW3-Result> from: %s", address[0])
                    self._serverIP = address[0]
                    self._serverPort = int(payload.split(";")[1])
                    logging.info("got connection info: %s:%d", self._serverIP, self._serverPort)
                    return True
            except socket.timeout:
                logging.warning("retry sending magic")
                continue
            except:
                logging.exception("error on getting connection info")
                return False

    @property
    def serverIP(self):
        return self._serverIP

    @property
    def serverPort(self):
        return self._serverPort


class BroadcastServer:
    """!General class comment"""

    def __init__(self, port=5000):
        """!init comment"""
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.bind(('', port))
        self._serverThread = None
        self._serverIsRunning = False

    def start(self):
        try:
            logging.debug("start udp broadcast server")
            self._serverThread = threading.Thread(target=self._listen)
            self._serverThread.name = "BroadServ"
            self._serverThread.daemon = True
            self._serverIsRunning = True
            self._serverThread.start()
        except:
            logging.exception("cannot start udp broadcast server thread")

    def stop(self):
        try:
            logging.debug("stop udp broadcast server")
            self._serverIsRunning = False
            self._serverThread.join()
        except:
            logging.exception("cannot stop udp broadcast server thread")

    def _listen(self):
        try:
            logging.debug("start listening for magic")
            while self._serverIsRunning:
                payload, address = self._socket.recvfrom(1024)
                payload = str(payload, "UTF-8")
                if payload == "<BW3-Request>":
                    logging.debug("received magic <BW3-Request> from: %s", address[0])
                    logging.info("send connection info in magic <BW3-Result> to: %s", address[0])
                    self._socket.sendto("<BW3-Result>;8080".encode(), address)  # todo give the TCPServer port
                    return True
        except:
            logging.exception("error while listening for clients")
