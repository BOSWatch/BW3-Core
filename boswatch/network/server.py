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

logging.debug("- %s loaded", __name__)

_clients = []  # module wide global list for received data sets


class TCPHandler(socketserver.BaseRequestHandler):
    """!RequestHandler class for our TCPServer class."""

    def handle(self):
        """!Handles the request from an single client in a own thread

        Insert a request in the clients[] list and send a [ack]"""
        data = 1
        cur_thread = threading.current_thread()
        req_name = str(cur_thread) + " " + self.client_address[0]

        try:
            while data:
                data = str(self.request.recv(1024).strip(), 'utf-8')
                if data is not "":
                    logging.debug(req_name + " recv: " + data)

                    # add a new entry at first position (index 0) with client IP
                    # and the decoded data dict as an string in utf-8
                    _clients.insert(0, (self.client_address[0], data))
                    logging.debug("Add data to queue")

                    logging.debug(req_name + " send: [ack]")
                    self.request.sendall(bytes("[ack]", "utf-8"))
            self.request.close()

        except (ConnectionResetError, ConnectionAbortedError):  # pragma: no cover
            logging.debug(req_name + " connection closed")
        except:  # pragma: no cover
            logging.exception(req_name + " error while receiving")


class TCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """!TCP server class"""

    def __init__(self, timeout=3):
        """!Create a new instance"""
        self._server = None
        self._server_thread = None
        self._timeout = timeout

    def start(self, port=8080):
        """!Start a threaded TCP socket server

        Start a TCP Socket Server in a new thread that will
        then start one more thread for each client request.
        The ip address for binding the server socket is always 'localhost'

        @param port: Server Port (8080)

        @return True or False"""
        try:
            self._server = socketserver.ThreadingTCPServer(("localhost", port), TCPHandler)
            self._server.timeout = self._timeout

            self.flushData()

            self._server_thread = threading.Thread(target=self._server.serve_forever)
            self._server_thread.daemon = True
            self._server_thread.start()
            logging.debug("TCPServer started in Thread: " + self._server_thread.name)
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
            self._server.socket.close()
            logging.debug("TCPServer stopped")
            return True
        except AttributeError:
            logging.exception("cannot stop - server not started?")
            return False
        except:  # pragma: no cover
            logging.exception("cannot stop the server")
            return False

    @staticmethod
    def clientsConnected():
        """!Number of currently connected Clients

        @todo works not safe atm
        @return Connected clients"""
        if threading.active_count() > 2:
            # must subtract the server() and the serve() Thread
            return threading.active_count() - 2
        else:
            return 0

    @staticmethod
    def getData():
        """!Function to get the data packages from server
        must be polled by main program

        @return Next data packet.py from intern queue"""
        if _clients:
            message = _clients.pop()
            logging.debug("Get data from queue")
            return message
        return None

    @staticmethod
    def flushData():
        """!To flush all existing data in queue"""
        logging.debug("Flush client data queue")
        _clients.clear()
