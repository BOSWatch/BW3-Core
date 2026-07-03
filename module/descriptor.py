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

@file:        descriptor.py
@date:        01.07.2026
@author:      Bastian Schroll
@description: Module to add descriptions to bwPackets with CSV and Regex support
"""
import logging
import csv
import re
import os
from module.moduleBase import ModuleBase

# ###################### #
# Custom plugin includes #

# ###################### #

logging.debug("- %s loaded", __name__)


class BoswatchModule(ModuleBase):
    r"""!Adds descriptions to bwPackets with CSV and Regex support"""
    def __init__(self, config):
        r"""!Do not change anything here!"""
        super().__init__(__name__, config)  # you can access the config class on 'self.config'

    def onLoad(self):
        r"""!Called by import of the plugin"""
        # Initialize unified cache for all descriptors
        self.unified_cache = {}

        # Process each descriptor configuration
        for descriptor_config in self.config:
            scan_field = descriptor_config.get("scanField")
            descr_field = descriptor_config.get("descrField")
            descriptor_key = f"{scan_field}_{descr_field}"

            # Register wildcard if specified
            if descriptor_config.get("wildcard", default=None):
                self.registerWildcard(descriptor_config.get("wildcard"), descr_field)

            # Initialize cache for this descriptor
            self.unified_cache[descriptor_key] = []

            # Load YAML descriptions first (for backward compatibility)
            yaml_descriptions = descriptor_config.get("descriptions", default=None)
            if yaml_descriptions:
                # yaml_descriptions is a Config object, we need to iterate properly
                for desc in yaml_descriptions:
                    entry = {
                        'for': str(desc.get("for", default="")),
                        'add': desc.get("add", default=""),
                        'isRegex': desc.get("isRegex", default=False)  # Default: False
                    }
                    # Handle string 'true'/'false' values
                    if isinstance(entry['isRegex'], str):
                        entry['isRegex'] = entry['isRegex'].lower() == 'true'

                    self.unified_cache[descriptor_key].append(entry)
                    logging.debug("Added YAML entry: %s -> %s", entry['for'], entry['add'])
                logging.info("Loaded %d YAML descriptions for %s", len(yaml_descriptions), descriptor_key)

            # Load CSV descriptions if csvPath is specified
            csv_path = descriptor_config.get("csvPath", default=None)
            if csv_path:
                self._load_csv_data(csv_path, descriptor_key)

            logging.info("Total entries for %s: %d", descriptor_key, len(self.unified_cache[descriptor_key]))

    def _load_csv_data(self, csv_path, descriptor_key):
        r"""!Load CSV data for a descriptor and add to unified cache"""
        try:
            if not os.path.isfile(csv_path):
                logging.error("CSV file not found: %s", csv_path)
                return

            csv_count = 0
            with open(csv_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Set default values if columns are missing
                    raw_for = str(row.get('for', '')).strip()
                    # Remove enclosing quotes
                    clean_for = raw_for.strip().strip('"').strip("'")
                    entry = {
                        'for': clean_for,
                        'add': row.get('add', '').strip(),
                        'isRegex': row.get('isRegex', 'false').lower() == 'true'  # Default: False
                    }
                    logging.debug("CSV row read: %s", row)
                    self.unified_cache[descriptor_key].append(entry)
                    csv_count += 1

            logging.info("Loaded %d entries from CSV: %s for %s", csv_count, csv_path, descriptor_key)

        except Exception as e:
            logging.error("Error loading CSV file %s: %s", csv_path, str(e))

    def _find_description(self, descriptor_key, scan_value, bw_packet):
        r"""!Find matching description for a scan value with Regex group support.

        The search is performed in two passes for performance optimization:
        1. First pass: Check for exact string matches (fast, no regex compilation)
        2. Second pass: Check regex patterns only if no exact match was found

        Regex patterns support capture groups that can be referenced in the description
        using standard regex backreferences (\1, \2, etc.) via match.expand().

        Example:
            Pattern: r"(\d{7})"
            Input: "1234567"
            Description template: "RIC: \1"
            Result: "RIC: 1234567"

        @param descriptor_key: Cache key identifying the descriptor configuration
        @param scan_value: Value to search for in the descriptor cache
        @param bw_packet: BOSWatch packet for wildcard replacement
        @return: Matched description string or None if no match found
        """

        descriptions = self.unified_cache.get(descriptor_key, [])
        scan_value_str = str(scan_value).strip()

        # First pass: Search for exact matches (performance optimization)
        # Exact matches are checked first because they don't require regex compilation
        for desc in descriptions:
            if not desc.get('isRegex', False):
                if desc['for'] == scan_value_str:
                    description_text = desc.get('add', '')
                    final_description = self._replace_wildcards(description_text, bw_packet)
                    return final_description

        # Second pass: Search for regex matches
        # Only executed if no exact match was found in the first pass
        for desc in descriptions:
            if desc.get('isRegex', False):
                match_pattern = desc.get('for', '')
                try:
                    match = re.search(match_pattern, scan_value_str)
                    if match:
                        description_text = desc.get('add', '')
                        # match.expand() replaces backreferences (\1, \2, etc.) with captured groups
                        # Example: pattern="(\d+)-(\d+)", input="123-456", template="First: \1, Second: \2"
                        #          result="First: 123, Second: 456"
                        expanded_description = match.expand(description_text)
                        final_description = self._replace_wildcards(expanded_description, bw_packet)
                        return final_description
                except re.error as e:
                    logging.error("Invalid regex pattern '%s': %s", match_pattern, e)

        return None

    def _replace_wildcards(self, text, bw_packet):
        r"""!Replace all available wildcards in description text dynamically."""
        if not text or '{' not in text:
            return text

        result = text

        # Search for wildcards in the format {KEY} and replace them with values from the bw_packet
        found_wildcards = re.findall(r"\{([A-Z0-9_]+)\}", result)

        for key in found_wildcards:
            key_lower = key.lower()
            value = bw_packet.get(key_lower)

            if value is not None:
                result = result.replace(f"{{{key}}}", str(value))
                logging.debug("Replaced wildcard {%s} with value '%s'", key, value)

        return result

    def doWork(self, bwPacket):
        r"""!start an run of the module.

        @param bwPacket: A BOSWatch packet instance"""
        logging.debug("Processing packet with mode: %s", bwPacket.get("mode"))

        # Process each descriptor configuration
        for descriptor_config in self.config:
            scan_field = descriptor_config.get("scanField")
            descr_field = descriptor_config.get("descrField")
            descriptor_key = f"{scan_field}_{descr_field}"

            logging.debug("Processing descriptor: scanField='%s', descrField='%s'", scan_field, descr_field)

            # Check if scanField is present in packet
            scan_value = bwPacket.get(scan_field)
            if scan_value is None:
                logging.debug("scanField '%s' not found in packet, skipping", scan_field)
                continue  # scanField not available in this packet - try next descriptor

            # Set default value (content of scanField)
            bwPacket.set(descr_field, str(scan_value))
            logging.debug("Set default value '%s' for field '%s'", scan_value, descr_field)

            # Search for matching description in unified cache
            description = self._find_description(descriptor_key, scan_value, bwPacket)

            if description is not None:
                bwPacket.set(descr_field, description)
                logging.info("Description set: '%s' -> '%s'", scan_value, description)
            else:
                logging.debug("No description found for value '%s' in field '%s'", scan_value, scan_field)

        logging.debug("Returning modified packet")
        return bwPacket

    def onUnload(self):
        r"""!Called by destruction of the plugin"""
        pass
