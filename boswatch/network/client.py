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

@file:        client.py
@date:        09.12.2017
@author:      Bastian Schroll
@description: Class implementation for a TCP socket client
"""
import logging
import socket
import select
from pprint import pformat

logging.debug("- %s loaded", __name__)

HEADERSIZE = 10


class TCPClient:
    """!TCP client class"""

    def __init__(self, timeout=3):
        """!Create a new instance

        @param timeout: timeout for the client in sec. (3)"""
        socket.setdefaulttimeout(timeout)
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host="localhost", port=8080):
        """!Connect to the server

        @param host: Server IP address ("localhost")
        @param port: Server Port (8080)
        @return True or False"""
        try:
            if not self.isConnected:
                self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self._sock.connect((host, port))
                logging.debug("connected to %s:%s", host, port)
                return True
            logging.warning("client always connected")
            return True
        except socket.error as e:
            logging.error(e)
        return False

    def disconnect(self):
        """!Disconnect from the server

        @return True or False"""
        try:
            if self.isConnected:
                self._sock.close()
                logging.debug("disconnected")
                return True
            logging.warning("client always disconnected")
            return True
        except socket.error as e:
            logging.error(e)
        return False

    def transmit(self, data):
        """!Send a data packet to the server

        @param data: data to send to the server
        @return True or False"""
        try:
            logging.debug("transmitting:\n%s", pformat(data))
            header = str(len(data)).ljust(HEADERSIZE)
            self._sock.sendall(bytes(header + data, "utf-8"))
            logging.debug("transmitted...")
            return True
        except socket.error as e:
            logging.error(e)
        return False

    def receive(self):
        """!Receive data from the server

        @return received data"""
        try:
            read, _, _ = select.select([self._sock], [], [], 1)
            if not read:  # check if there is something to read
                return False
            header = self._sock.recv(HEADERSIZE)
            if not len(header):  # check if there data
                return False
            logging.debug("recv header: '%s'", header)
            length = int(header.decode("utf-8").strip())
            received = self._sock.recv(length).decode("utf-8")
            logging.debug("received %d bytes: %s", length, received)
            return received
        except socket.error as e:
            logging.error(e)
        return False

    @property
    def isConnected(self):
        """!Property of client connected state"""
        _, write, _ = select.select([], [self._sock], [], 0.1)
        if write:
            return True
        return False
