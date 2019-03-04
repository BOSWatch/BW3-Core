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

@file:        route.py
@date:        04.03.2019
@author:      Bastian Schroll
@description: Class for a single BOSWatch packet router route point
"""


class Route:
    """!Class for single routing points"""
    def __init__(self, name, callback):
        """!Create a instance of an route point

        @param name: name of the route point
        @param callback: instance of the callback function
        """
        self._name = name
        self._callback = callback

    @property
    def name(self):
        """!Property to get the route point name"""
        return self._name

    @property
    def callback(self):
        """!Porperty to get the callback function instance"""
        return self._callback
