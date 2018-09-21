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

@file:        server.py
@date:        11.12.2017
@author:      Bastian Schroll
@description: Class implementation for a threaded TCP socket server
"""
import logging
import socketserver
import threading
import time

logging.debug("- %s loaded", __name__)


class ThreadedTCPRequestHandler(socketserver.ThreadingMixIn, socketserver.BaseRequestHandler):
    """!ThreadedTCPRequestHandler class for our TCPServer class."""

    def handle(self):
        """!Handles the request from an single client in a own thread

        Insert a request in the clients[] list and send a [ack]"""
        with self.server.clientsConnctedLock:  # because our list is not threadsafe
            self.server.clientsConnected[threading.current_thread().name] = {"address": self.client_address[0], "timestamp": time.time()}

        logging.info("Client connected: %s", self.client_address[0])
        data = 1  # to enter while loop
        cur_thread = threading.current_thread().name
        req_name = str(cur_thread) + " " + self.client_address[0]

        try:
            while data:
                data = str(self.request.recv(1024).strip(), 'utf-8')
                if data != "":
                    logging.debug("%s recv: %s", req_name, data)

                    # add a new entry and the decoded data dict as an string in utf-8 and an timestamp
                    self.server.alarmQueue.put_nowait((self.client_address[0], data, time.time()))  # queue is threadsafe
                    logging.debug("Add data to queue")

                    logging.debug("%s send: [ack]", req_name)
                    self.request.sendall(bytes("[ack]", "utf-8"))
            self.request.close()

        except (ConnectionResetError, ConnectionAbortedError):  # pragma: no cover
            logging.debug("%s connection closed", req_name)
        except:  # pragma: no cover
            logging.exception("%s error while receiving", req_name)
        finally:
            del self.server.clientsConnected[threading.current_thread().name]
            logging.info("Client disconnected: %s", self.client_address[0])


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """!ThreadedTCPServer class for our TCPServer class."""
    pass


class TCPServer:
    """!TCP server class"""

    def __init__(self, alarmQueue, timeout=3):
        """!Create a new instance

        @param alarmQueue: python queue instance
        @param timeout: server timeout in sec (3)
        """
        self._server = None
        self._server_thread = None
        self._timeout = timeout
        self._alarmQueue = alarmQueue

        self._clientsConnectedLock = threading.Lock()
        self._clientsConnected = {}

    def start(self, port=8080):
        """!Start a threaded TCP socket server

        Start a TCP Socket Server in a new thread that will
        then start one more thread for each client request.
        The ip address for binding the server socket is always 'localhost'

        @param port: Server Port (8080)

        @return True or False"""
        try:
            self._server = ThreadedTCPServer(("", port), ThreadedTCPRequestHandler)
            self._server.timeout = self._timeout
            self._server.alarmQueue = self._alarmQueue

            self._server.clientsConnctedLock = self._clientsConnectedLock
            self._server.clientsConnected = self._clientsConnected

            self._server_thread = threading.Thread(target=self._server.serve_forever)
            self._server_thread.name = "Thread-BWServer"
            self._server_thread.daemon = True
            self._server_thread.start()
            logging.debug("TCPServer started in Thread: %s", self._server_thread.name)
            return True
        except OSError:
            logging.exception("server always running?")
        except:  # pragma: no cover
            logging.exception("cannot start the server")
            return False

    def stop(self):
        """!Stops the TCP socket server

        @return True or False"""
        try:
            self._server.shutdown()
            self._server_thread.join()
            self._server_thread = None
            self._server.socket.close()
            self._server = None
            logging.debug("TCPServer stopped")
            return True
        except AttributeError:
            logging.exception("cannot stop - server not started?")
            return False
        except:  # pragma: no cover
            logging.exception("cannot stop the server")
            return False

    def countClientsConnected(self):
        """!Number of currently connected Clients

        @return Connected clients"""
        with self._clientsConnectedLock:  # because our list is not threadsafe
            return len(self._clientsConnected)

    def getClientsConnected(self):
        """!A list of all connected clients
        with their IP address and last seen timestamp
        _clients[ThreadName] = {"address", "timestamp"}

        @return List of onnected clients"""
        # todo return full list or write a print/debug method?
        with self._clientsConnectedLock:  # because our list is not threadsafe
            return self.clientsConnected
