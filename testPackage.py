#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import socket
import select

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
        """!Send a data packet to the server

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
        """!Receive data from the server

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
        """!Property of client connected state"""
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

client = TCPClient()
client.connect()
client.transmit(str({
    'serverName': 'TestServer',
    'serverVersion': '3.0',
    'serverBuildDate': '01.01.2020',
    'serverBranch': 'develop',
    'clientName': 'TestClient',
    'clientIP': '127.0.0.1',
    'clientVersion': '3.0',
    'clientBuildDate': '01.01.2020',
    'clientBranch': 'develop',
    'inputSource': 'sdr',
    'timestamp': '15:30',
    'frequency': '173.240',
    'mode': 'pocsag',
    'bitrate': '512',
    'ric': '1326089',
    'subric': '1',
    'subricText': 'a',
    'message': '17:22 FW 18865 Gebäudebrand_kle Sandkampstr.,15,-,Hopsten,NRW rauchentwicklung'
}))