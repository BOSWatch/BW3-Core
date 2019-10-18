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
    """!class to manage a extern sub process"""
    def __init__(self, process, textMode=False):
        logging.debug("create process instance %s - textMode: %s", process, textMode)
        self._args = []
        self._args.append(process)
        self._stdin = None
        self._stdout = subprocess.PIPE
        self._stderr = subprocess.STDOUT
        self._processHandle = None
        self._textMode = textMode

    def __del__(self):
        self.stop()

    def addArgument(self, arg):
        """!add a new argument

        @param arg: argument to add as string"""
        logging.debug("add argument to process: %s -> %s", self._args[0], arg)
        for splitArg in arg.split():
            self._args.append(splitArg)

    def clearArguments(self):
        """!clear all arguments"""
        self._args = self._args[0:1]  # kept first element (process name)

    def start(self):
        """!start the new process

        @return: True or False"""
        logging.debug("start new process: %s %s", self._args[0], self._args[1:])
        try:
            self._processHandle = subprocess.Popen(self._args,
                                                   stdin=self._stdin,
                                                   stdout=self._stdout,
                                                   stderr=self._stderr,
                                                   universal_newlines=self._textMode,
                                                   shell=False)
            if not self.isRunning:
                logging.error("cannot start")
                return False
            logging.debug("process started with PID %d", self._processHandle.pid)
            return True

        except FileNotFoundError:
            logging.error("File not found: %s", self._args[0])
            return False

    def stop(self):
        """!Stop the process by sending SIGTERM and wait for ending"""
        logging.debug("stopping process: %s", self._args[0])
        if self.isRunning:
            self._processHandle.terminate()
            while self.isRunning:
                pass
        logging.debug("process %s returned %d", self._args[0], self._processHandle.returncode)

    def readline(self):
        """!Read one line from stdout stream

        @return singe line or None"""
        if self.isRunning and self._stdout is not None:
            try:
                line = self._processHandle.stdout.readline().strip()
            except UnicodeDecodeError:
                return None

            return line
        return None

    def skipLines(self, lineCount=1):
        """!Skip given number of lines from the output

        @param lineCount: number of lines to skip
        """
        logging.debug("skip %d lines from output", lineCount)
        while lineCount:
            self.readline()
            lineCount -= 1

    def skipLinesUntil(self, matchText):
        """!Skip lines from the output until the given string is in it

        @param matchText: string to search for in output
        """
        logging.debug("skip lines till %s from output", matchText)
        while matchText not in self.readline():
            pass

    def setStdin(self, stdin):
        """!Set the stdin stream instance"""
        self._stdin = stdin

    def setStdout(self, stdout):
        """!Set the stdout stream instance"""
        self._stdout = stdout

    def setStderr(self, stderr):
        """!Set the stderr stream instance"""
        self._stderr = stderr

    @property
    def stdout(self):
        """!Property to get the stdout stream"""
        return self._processHandle.stdout

    @property
    def stderr(self):
        """!Property to get the stderr stream"""
        return self._processHandle.stderr

    @property
    def isRunning(self):
        """!Property to get process running state

        @return True or False"""
        if self._processHandle:
            if self._processHandle.poll() is None:
                return True
        return False
