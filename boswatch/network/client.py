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

logging.debug("- %s loaded", __name__)


class TCPClient:
    """!TCP client class"""

    def __init__(self, timeout=3):
        """!Create a new instance

        Create a new instance of an TCP Client.
        And set the timeout"""
        try:
            self._sock = None
            self._timeout = timeout
        except:  # pragma: no cover
            logging.exception("cannot create a TCPClient")

    def connect(self, host="localhost", port=8080):
        """!Connect to the server

        @param host: Server IP address (localhost)
        @param port: Server Port (8080)
        @return True or False"""
        try:
            self._sock = socket
            self._sock.setdefaulttimeout(self._timeout)
            self._sock = socket.create_connection((host, port))

            logging.debug("connected to " + str(host) + ":" + str(port))
            return True
        except ConnectionRefusedError:
            logging.error("cannot connect to %s:%s - connection refused", str(host), str(port))
            return False
        except socket.timeout:  # pragma: no cover
            logging.warning("cannot connect to %s:%s - timeout after %s sec", str(host), str(port), self._timeout)
            return False
        except:  # pragma: no cover
            logging.exception("cannot connect to %s:%s", str(host), str(port))
            return False

    def disconnect(self):
        """!Disconnect from the server

        @return True or False"""
        try:
            self._sock.close()
            logging.debug("disconnected")
            return True
        except AttributeError:
            logging.error("cannot disconnect - no connection established")
            return False
        except:  # pragma: no cover
            logging.exception("error while disconnecting")
            return False

    def transmit(self, data):
        """!Send a data packet to the server

        @param data: data to send to the server
        @return True or False"""
        try:
            logging.debug("transmitting: " + data)
            self._sock.sendall(bytes(data + "\n", "utf-8"))
            logging.debug("transmitted...")
            return True
        except AttributeError:
            logging.error("cannot transmit - no connection established")
            return False
        except ConnectionResetError:
            logging.error("cannot transmit - host closed connection")
            return False
        except:  # pragma: no cover
            logging.exception("error while transmitting")
            return False

    def receive(self):
        """!Receive data from the server

        @return received data"""
        try:
            received = str(self._sock.recv(1024), "utf-8")
            logging.debug("received: " + received)
            return received
        except AttributeError:
            logging.error("cannot receive - no connection established")
            return False
        except ConnectionResetError:
            logging.error("cannot receive - host closed connection")
            return False
        except socket.timeout:  # pragma: no cover
            logging.warning("cannot receive - timeout after %s sec", self._timeout)
            return False
        except:  # pragma: no cover
            logging.exception("error while receiving")
            return False
