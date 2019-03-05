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

@file:        processManager.py
@date:        04.03.2018
@author:      Bastian Schroll
@description: Class for managing sub processes
"""
import logging
import subprocess

logging.debug("- %s loaded", __name__)


class ProcessManager:
    def __init__(self, process, textMode=False):
        self._args = []
        self._args.append(process)
        self._stdin = None
        self._stdout = subprocess.PIPE
        self._stderr = subprocess.STDOUT
        self._processHandle = None
        self._textMode = textMode
        pass

    def addArgument(self, arg):
        self._args.append(arg)

    def clearArguments(self):
        self._args = []

    def run(self):
        self._processHandle = subprocess.Popen(self._args,
                                               stdin=self._stdin,
                                               stdout=self._stdout,
                                               stderr=self._stderr,
                                               shell=False,
                                               universal_newlines=self._textMode)

    def stop(self):
        if self._processHandle and self.isRunning:
            self._processHandle.terminate()
        while self.isRunning:
            pass

    def readline(self):
        """!Read one line from stdout stream or None"""
        if self.isRunning and self._stdout is not None:
            try:
                line = self._processHandle.stdout.readline().strip()
            except UnicodeDecodeError:
                return None
            if line != "":
                return line
        return None

    def setStdin(self, stdin):
        """!Set the stdin stream"""
        self._stdin = stdin

    def setStdout(self, stdout):
        """!Set the stdout stream"""
        self._stdout = stdout

    def setStderr(self, stderr):
        """!Set the stderr stream"""
        self._stderr = stderr

    @property
    def stdout(self):
        """!Get the stdout stream"""
        return self._processHandle.stdout

    @property
    def stderr(self):
        """!Get the stderr stream"""
        return self._processHandle.stderr

    @property
    def isRunning(self):
        if self._processHandle:
            if self._processHandle.poll() is None:
                return True
        return False
