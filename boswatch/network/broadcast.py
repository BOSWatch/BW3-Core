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
    """!BroadcastClient class"""

    def __init__(self, port=5000):
        """!Create an BroadcastClient instance

        @param port: port to send broadcast packets (5000)"""
        self._broadcastPort = port

        self._serverIP = ""
        self._serverPort = 0

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self._socket.settimeout(5)

    def sendBroadcast(self):
        """!Send broadcastpackets

        This function will block until the connection Info
        from server will be received.

        - send the magic packet <BW-Request> on broadcast address.
        - wait for a <BW-Result> magic packet.
        - extract the connection data from the magic packet and return

        @return True or False"""
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
                logging.warning("no server found - retry sending magic")
                continue
            except:
                logging.exception("error on getting connection info")
                return False

    @property
    def serverIP(self):
        """!Property to get the server IP after successful broadcast"""
        return self._serverIP

    @property
    def serverPort(self):
        """!Property to get the server Port after successful broadcast"""
        return self._serverPort


class BroadcastServer:
    """!BroadcastServer class"""

    def __init__(self, servePort=8080,listenPort=5000):
        """!Create an BroadcastServer instance

        @param listenPort: port to listen for broadcast packets (5000)"""
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self._socket.bind(('', listenPort))
        self._serverThread = None
        self._serverIsRunning = False
        self._servePort = servePort

    def start(self):
        """!Start the broadcast server in a new thread

        @return True or False"""
        try:
            logging.debug("start udp broadcast server")
            self._serverThread = threading.Thread(target=self._listen)
            self._serverThread.name = "BroadServ"
            self._serverThread.daemon = True
            self._serverIsRunning = True
            self._serverThread.start()
            return True
        except:
            logging.exception("cannot start udp broadcast server thread")
            return False

    def stop(self):
        """!Stop the broadcast server

        @return True or False"""
        try:
            logging.debug("stop udp broadcast server")
            self._serverIsRunning = False
            self._serverThread.join()
            return True
        except:
            logging.exception("cannot stop udp broadcast server thread")
            return False

    def _listen(self):
        """!Broadcast server worker thread

        This function listen for magic packets on broadcast
        address and send the connection info to the clients.

        - listen for the magic packet <BW-Request>
        - send connection info in an <BW-Result> macig packet"""
        try:
            logging.debug("start listening for magic")
            while self._serverIsRunning:
                payload, address = self._socket.recvfrom(1024)  # fixme recv is blocking, evtl we can use to wait for readable data
                payload = str(payload, "UTF-8")
                if payload == "<BW3-Request>":
                    logging.debug("received magic <BW3-Request> from: %s", address[0])
                    logging.info("send connection info in magic <BW3-Result> to: %s", address[0])
                    self._socket.sendto("<BW3-Result>;".encode() + str(self._servePort).encode(), address)
        except:
            logging.exception("error while listening for clients")
