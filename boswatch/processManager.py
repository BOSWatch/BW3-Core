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
    def __init__(self, process):
        self._args = []
        self._args.append(process)
        self._stdin = None
        self._stdout = subprocess.PIPE
        self._stderr = subprocess.PIPE
        self._processHandle = None
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
                                               shell=True)

    def readline(self):
        """!Read one line from stdout stream or None"""
        if self._stdout is not None:
            return self._processHandle.stdout.readline().strip()
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
