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

@file:        descriptor.py
@date:        07.01.2018
@author:      Bastian Schroll
@description: Descriptor to load Descriptions from csv files
"""
import logging
import csv
import re

from boswatch.utils import paths

logging.debug("- %s loaded", __name__)


class Descriptor:
    """!CSV Descriptor class to load specific
    descriptions from CSV files, manage and serve them"""

    def __init__(self):
        """!Initialise a private list for the DescriptionList objects"""
        self._lists = {}

    def loadDescription(self, csvType):
        """!Build a new description list from DescriptionList class

        @param csvType: Name of the CSV file without `.csv`
        @return True or False"""
        bwDescriptionList = DescriptionList()
        if bwDescriptionList.loadCSV(csvType):
            self._lists[csvType] = bwDescriptionList
            return True
        return False

    def addDescriptions(self, bwPacket):
        """!Add the short and long description to a bwPacket

        @param bwPacket: bwPacket instance to add descriptions
        @return True or False"""
        logging.debug("add descriptions to bwPacket")
        try:
            bwPacket.set("shortDescription",
                         self._lists[bwPacket.get("mode")].getShortDescription(bwPacket.get(bwPacket.get("mode"))))

            bwPacket.set("longDescription",
                         self._lists[bwPacket.get("mode")].getLongDescription(bwPacket.get(bwPacket.get("mode"))))
            return True
        except:  # pragma: no cover
            logging.exception("error while adding descriptions")
            return False


class DescriptionList:
    def __init__(self):
        """!Loads the given CSV file into internal list"""
        logging.debug("create new descriptionList")
        self._descriptionList = {}

    def getShortDescription(self, checkId):
        """!Returns the short description of given id

        @return short description or empty string"""
        try:
            return self._descriptionList[str(checkId)]["shortDescription"]
        except:
            return ""

    def getLongDescription(self, checkId):
        """!Returns the long description of given id

        @return long description or empty string"""
        try:
            return self._descriptionList[str(checkId)]["longDescription"]
        except:
            return ""

    def loadCSV(self, csvType):
        """!Load descriptions from an csv file

        @param csvType: Name of the CSV file without `.csv`
        @return True or False"""
        count = 0
        logging.debug("loading csv file: %s", csvType)
        csvPath = paths.CSV_PATH + csvType + ".csv"
        try:
            csvFile = open(csvPath, 'r', -1, 'utf-8')
            reader = csv.DictReader(csvFile)

            for line in reader:
                if re.match("^[0-9]+[A-D]?$", line["id"], re.IGNORECASE):
                    self._descriptionList[line["id"]] = {"shortDescription": line["shortDescription"], "longDescription": line["longDescription"]}
                    logging.debug("- %s", line)
                    count += 1

            logging.debug("%s entry's loaded", count)
            return True
        except FileNotFoundError:
            logging.error("csv file not found: %s", csvPath)
            return False
        except:  # pragma: no cover
            logging.exception("error while loading descriptions")
            return False
