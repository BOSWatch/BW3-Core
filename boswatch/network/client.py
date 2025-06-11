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

@file:        client.py
@date:        09.12.2017
@author:      Bastian Schroll
@description: Class implementation for a TCP socket client
"""
import logging
import socket
import select

logging.debug("- %s loaded", __name__)

HEADERSIZE = 10


class TCPClient:
    r"""!TCP client class"""

    def __init__(self, timeout=3):
        r"""!Create a new instance

        @param timeout: timeout for the client in sec. (3)"""
        socket.setdefaulttimeout(timeout)
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host="localhost", port=8080):
        r"""!Connect to the server

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
        r"""!Disconnect from the server

        @return True or False"""
        try:
            if self.isConnected:
                self._sock.shutdown(socket.SHUT_RDWR)
                self._sock.close()
                logging.debug("disconnected")
                return True
            logging.warning("client always disconnected")
            return True
        except socket.error as e:
            logging.error(e)
        return False

    def transmit(self, data):
        r"""!Send a data packet to the server

        @param data: data to send to the server
        @return True or False"""
        try:
            logging.debug("transmitting:\n%s", data)
            data = data.encode("utf-8")
            header = str(len(data)).ljust(HEADERSIZE).encode("utf-8")
            self._sock.sendall(header + data)
            logging.debug("transmitted...")
            return True
        except socket.error as e:
            logging.error(e)
        return False

    def receive(self, timeout=1):
        r"""!Receive data from the server

        @param timeout: to wait for incoming data in seconds
        @return received data"""
        try:
            read, _, _ = select.select([self._sock], [], [], timeout)
            if not read:  # check if there is something to read
                return False

            header = self._sock.recv(HEADERSIZE).decode("utf-8")
            if not len(header):  # check if there data
                return False

            length = int(header.strip())
            received = self._sock.recv(length).decode("utf-8")

            logging.debug("recv header: '%s'", header)
            logging.debug("received %d bytes: %s", len(received), received)
            return received
        except socket.error as e:
            logging.error(e)
        return False

    @property
    def isConnected(self):
        r"""!Property of client connected state"""
        try:
            if self._sock:
                _, write, _ = select.select([], [self._sock], [], 0.1)
                if write:
                    data = "<keep-alive>".encode("utf-8")
                    header = str(len(data)).ljust(HEADERSIZE).encode("utf-8")
                    self._sock.sendall(header + data)
                    return True
            return False
        except socket.error as e:
            if e.errno != 32:
                logging.exception(e)
            return False
        except ValueError:
            return False
