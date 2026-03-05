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

@file:        multicast.py
@date:        26.01.2025
@author:      Claus Schichl
@description: multicast module
"""

import logging
import time
import threading
import json
import datetime
from collections import defaultdict
from module.moduleBase import ModuleBase
from boswatch.packet import Packet
from boswatch.network.client import TCPClient

logging.debug("- %s loaded", __name__)


class BoswatchModule(ModuleBase):
    r"""!Multicast module with multi-instance support and active trigger mechanism

    This module handles multicast alarm distribution.
    It manages the correlation between tone-RICs (recipients) and text-RICs (message content),
    ensuring reliable alarm delivery even in complex multi-frequency scenarios.
    """

    # CLASS VARIABLES - SHARED STATE
    _tone_ric_packets = defaultdict(list)
    _last_tone_ric_time = defaultdict(float)
    _processing_text_ric = defaultdict(bool)
    _processing_text_ric_started = defaultdict(float)

    # SYSTEM VARIABLES
    _lock = threading.Lock()
    _cleanup_thread = None
    _running = False
    _wildcards_registered = set()
    _packet_queue = []
    _queue_lock = threading.Lock()
    _instances = []

    # Trigger defaults
    _TRIGGER_HOST = "127.0.0.1"
    _TRIGGER_PORT = 8080
    _MAGIC_WAKEUP_MSG = "###_MULTICAST_WAKEUP_###"
    _DEFAULT_TRIGGER_RIC = "9999999"

# ============================================================
# LIFECYCLE METHODS
# ============================================================

    def __init__(self, config):
        super().__init__(__name__, config)

    def onLoad(self):
        r"""!Initialize module configuration and start the global cleanup thread.

        @param None
        @return None"""
        self._my_frequencies = set()
        self.instance_id = hex(id(self))[-4:]
        self.name = f"MCAST_{self.instance_id}"

        self._auto_clear_timeout = int(self.config.get("autoClearTimeout", default=10))
        self._hard_timeout = self._auto_clear_timeout * 3

        def parse_list(key):
            val = self.config.get(key)
            if val:
                return [x.strip() for x in str(val).split(",") if x.strip()]
            return []

        self._delimiter_rics = parse_list("delimiterRics")
        self._text_rics = parse_list("textRics")
        self._netident_rics = parse_list("netIdentRics")

        trigger_ric_cfg = self.config.get("triggerRic")
        if trigger_ric_cfg:
            self._trigger_ric = str(trigger_ric_cfg).strip()
            self._trigger_ric_mode = "explicit"
        else:
            self._trigger_ric = None
            self._trigger_ric_mode = "dynamic"

        self._trigger_host = self.config.get("triggerHost", default=self._TRIGGER_HOST)
        self._trigger_port = int(self.config.get("triggerPort", default=self._TRIGGER_PORT))

        self._block_delimiter = bool(self._delimiter_rics)
        self._block_netident = bool(self._netident_rics)

        logging.info("[%s] Multicast module loaded", self.name)

        with BoswatchModule._lock:
            if self not in BoswatchModule._instances:
                BoswatchModule._instances.append(self)

            if not BoswatchModule._running:
                BoswatchModule._running = True
                BoswatchModule._cleanup_thread = threading.Thread(
                    target=BoswatchModule._global_cleanup_worker, daemon=True
                )
                BoswatchModule._cleanup_thread.start()
                logging.info("Global multicast cleanup thread started")

# ============================================================
# MAIN PROCESSING
# ============================================================

    def doWork(self, bwPacket):
        r"""!Process an incoming packet and handle multicast logic.

        @param bwPacket: A BOSWatch packet instance or list of packets
        @return bwPacket, a list of packets, or False if blocked"""
        if isinstance(bwPacket, list):
            result_packets = []
            for single_packet in bwPacket:
                processed = self.doWork(single_packet)
                if processed is None:
                    result_packets.append(single_packet)
                elif processed is not False:
                    if isinstance(processed, list):
                        result_packets.extend(processed)
                    else:
                        result_packets.append(processed)
            return result_packets if result_packets else None

        packet_dict = self._get_packet_data(bwPacket)
        msg = packet_dict.get("message")
        ric = packet_dict.get("ric")
        freq = packet_dict.get("frequency", "default")
        mode = packet_dict.get("mode")

        if msg == BoswatchModule._MAGIC_WAKEUP_MSG:
            if self._trigger_ric and ric != self._trigger_ric:
                pass
            else:
                logging.debug("[%s] Wakeup trigger received (RIC=%s)", self.name, ric)
                queued = self._get_queued_packets()
                return queued if queued else False

        if mode != "pocsag":
            queued = self._get_queued_packets()
            return queued if queued else None

        self._my_frequencies.add(freq)

        is_text_ric = False
        if self._text_rics:
            is_text_ric = ric in self._text_rics and msg and msg.strip()
        else:
            with BoswatchModule._lock:
                is_text_ric = msg and msg.strip() and len(BoswatchModule._tone_ric_packets[freq]) > 0

        if is_text_ric:
            with BoswatchModule._lock:
                BoswatchModule._processing_text_ric[freq] = True
                BoswatchModule._processing_text_ric_started[freq] = time.time()

        queued_packets = self._get_queued_packets()
        incomplete_packets = None if is_text_ric else self._check_instance_auto_clear(freq)

        if self._netident_rics and ric in self._netident_rics:
            self._set_mcast_metadata(bwPacket, "control", "netident", ric)
            result = self._combine_results(incomplete_packets, queued_packets, [bwPacket])
            return self._filter_output(result)

        if self._delimiter_rics and ric in self._delimiter_rics:
            delimiter_incomplete = self._handle_delimiter(freq, ric, bwPacket)
            result = self._combine_results(delimiter_incomplete, incomplete_packets, queued_packets)
            return self._filter_output(result)

        if not msg or not msg.strip():
            self._add_tone_ric_packet(freq, packet_dict)
            result = self._combine_results(incomplete_packets, queued_packets, False)
            return self._filter_output(result)

        if is_text_ric and msg:
            logging.info("[%s] Text-RIC received: RIC=%s", self.name, ric)
            alarm_packets = self._distribute_complete(freq, packet_dict)
            with BoswatchModule._lock:
                BoswatchModule._processing_text_ric[freq] = False
                BoswatchModule._processing_text_ric_started.pop(freq, None)

            if not alarm_packets:
                logging.warning("[%s] No tone-RICs for text-RIC=%s", self.name, ric)
                normal = self._enrich_normal_alarm(bwPacket, packet_dict)
                result = self._combine_results(normal, incomplete_packets, queued_packets)
            else:
                result = self._combine_results(alarm_packets, incomplete_packets, queued_packets)
            return self._filter_output(result)

        if msg:
            normal = self._enrich_normal_alarm(bwPacket, packet_dict)
            result = self._combine_results(normal, incomplete_packets, queued_packets)
            return self._filter_output(result)

        result = self._combine_results(incomplete_packets, queued_packets)
        return self._filter_output(result)

# ============================================================
# PACKET PROCESSING HELPERS (called by doWork)
# ============================================================

    def _get_packet_data(self, bwPacket):
        r"""!Safely extract all fields from packet as a dictionary.

        Handles both dict objects and Packet instances.
        Dynamically extracts all fields including those added by other modules.

        @param bwPacket: Packet instance or dict
        @return dict: Complete dictionary of all packet fields"""
        # 1. Fall: Es ist bereits ein Dictionary
        if isinstance(bwPacket, dict):
            return bwPacket.copy()

        # 2. Fall: Es ist ein Packet-Objekt (Daten liegen in _packet)
        if hasattr(bwPacket, '_packet'):
            return bwPacket._packet.copy()

        # 3. Fallback: Falls es ein anderes Objekt ist, versuche __dict__ ohne '_' Filter für 'packet'
        try:
            return {k: v for k, v in bwPacket.__dict__.items() if not k.startswith('_')}
        except Exception as e:
            logging.warning("[%s] Error: %s", self.name, e)
            return {}

    def _filter_output(self, result):
        r"""!Apply multicastRole filtering before output.

        @param result: Single packet, list of packets, None or False
        @return Final packet(s) or False if blocked"""
        if result is None or result is False:
            return result

        def get_role(packet):
            """Helper to extract multicastRole from Packet object"""
            packet_dict = self._get_packet_data(packet)
            return packet_dict.get("multicastRole")

        if isinstance(result, list):
            filtered = [p for p in result if self._should_output_packet(get_role(p))]
            if not filtered:
                logging.debug("All packets filtered out by multicastRole")
                return False
            return filtered if len(filtered) > 1 else filtered[0]
        else:
            if self._should_output_packet(get_role(result)):
                return result
            logging.debug("Packet filtered out: multicastRole=%s", get_role(result))
            return False

    def _combine_results(self, *results):
        r"""!Combine multiple result sources into a single list or status.

        @param results: Multiple packet objects, lists, or booleans
        @return combined list, False or None"""
        combined = []
        has_false = False
        for result in results:
            if result is False:
                has_false = True
                continue
            if result is None:
                continue
            if isinstance(result, list):
                combined.extend(result)
            else:
                combined.append(result)
        if combined:
            return combined
        return False if has_false else None

    def _should_output_packet(self, multicast_role):
        r"""!Check if packet should be output based on role.

        @param multicast_role: The role string to check
        @return bool: True if allowed"""
        if self._block_delimiter and multicast_role == "delimiter":
            return False
        if self._block_netident and multicast_role == "netident":
            return False
        return True

# ============================================================
# TONE-RIC BUFFER MANAGEMENT
# ============================================================

    def _add_tone_ric_packet(self, freq, packet_dict):
        r"""!Add a tone-RIC to the shared buffer.

        @param freq: Frequency identifier
        @param packet_dict: Dictionary containing packet data
        @return None"""
        with BoswatchModule._lock:
            stored_packet = packet_dict.copy()
            stored_packet['_multicast_timestamp'] = time.time()
            BoswatchModule._tone_ric_packets[freq].append(stored_packet)
            BoswatchModule._last_tone_ric_time[freq] = stored_packet['_multicast_timestamp']
            logging.debug("[%s] Tone-RIC added: RIC=%s (total: %d on %s)", self.name, stored_packet.get('ric'), len(BoswatchModule._tone_ric_packets[freq]), freq)

    def _get_queued_packets(self):
        r"""!Pop and return all packets currently in the static queue.

        @param None
        @return list: List of packets or None"""
        with BoswatchModule._queue_lock:
            if BoswatchModule._packet_queue:
                packets = BoswatchModule._packet_queue[:]
                BoswatchModule._packet_queue.clear()
                return packets
        return None

# ============================================================
# MULTICAST PACKET CREATION
# ============================================================

    def _copy_packet_dict_to_packet(self, recipient_dict, packet, index=1):
        r"""!Copy dict fields to Packet with timestamp shift for DB uniqueness.

        @param recipient_dict: Source dictionary
        @param packet: Target Packet object
        @param index: Packet index (1-based) - shifts timestamp by milliseconds
        @return None"""
        for k, v in recipient_dict.items():
            if k.startswith('_'):
                continue
            if k == 'timestamp' and index > 1:
                try:
                    dt = datetime.datetime.strptime(str(v), '%d.%m.%Y %H:%M:%S')
                    dt_shifted = dt + datetime.timedelta(milliseconds=index - 1)
                    packet.set(k, dt_shifted.strftime('%d.%m.%Y %H:%M:%S'))
                except:
                    packet.set(k, str(v))
            else:
                packet.set(k, str(v))

    def _distribute_complete(self, freq, text_packet_dict):
        r"""!Create full multicast packets with message content.

        @param freq: Frequency identifier
        @param text_packet_dict: Data of the message-carrying packet
        @return list: List of fully populated Packet instances"""
        with BoswatchModule._lock:
            recipient_dicts = BoswatchModule._tone_ric_packets[freq].copy()
            logging.debug("Text-RIC gefunden. Matche gegen %d gespeicherte RICs", len(recipient_dicts))
            BoswatchModule._tone_ric_packets[freq].clear()
            BoswatchModule._last_tone_ric_time.pop(freq, None)

        if not recipient_dicts:
            return []
        text_ric = text_packet_dict.get("ric")
        message_text = text_packet_dict.get("message")
        alarm_packets = []

        for idx, recipient_dict in enumerate(recipient_dicts, 1):
            p = Packet()
            self._copy_packet_dict_to_packet(recipient_dict, p, idx)
            p.set("message", message_text)
            self._apply_list_tags(p, recipient_dicts)
            self._set_mcast_metadata(p, "complete", "recipient", text_ric, len(recipient_dicts), idx)
            alarm_packets.append(p)

        logging.info("[%s] Generated %d complete multicast packets for text-RIC %s", self.name, len(alarm_packets), text_ric)
        return alarm_packets

    def _create_incomplete_multicast(self, freq, recipient_dicts):
        r"""!Generate multicast packets for timeouts (no text message).

        @param freq: Frequency identifier
        @param recipient_dicts: List of recipient data dictionaries
        @return list: List of incomplete Packet instances"""
        if not recipient_dicts:
            return []
        first_ric = recipient_dicts[0].get("ric", "unknown")
        incomplete_packets = []
        for idx, recipient_dict in enumerate(recipient_dicts, 1):
            p = Packet()
            self._copy_packet_dict_to_packet(recipient_dict, p, idx)
            p.set("message", "")
            self._apply_list_tags(p, recipient_dicts)
            self._set_mcast_metadata(p, "incomplete", "recipient", first_ric, len(recipient_dicts), idx)
            incomplete_packets.append(p)
        return incomplete_packets

    def _enrich_normal_alarm(self, bwPacket, packet_dict):
        r"""!Enrich a standard single alarm with multicast metadata.

        @param bwPacket: Target Packet object
        @param packet_dict: Source data dictionary
        @return list: List containing the enriched packet"""
        self._copy_packet_dict_to_packet(packet_dict, bwPacket, index=1)
        self._apply_list_tags(bwPacket, [packet_dict])
        self._set_mcast_metadata(bwPacket, "single", "single", packet_dict.get("ric", ""), "1", "1")
        logging.debug(f"Erstelle Single-Alarm für RIC {packet_dict.get('ric')}")
        return [bwPacket]

    def _handle_delimiter(self, freq, ric, bwPacket=None):
        r"""!Handle delimiter packet and clear orphaned tone-RICs.

        @param freq: Frequency identifier
        @param ric: Delimiter RIC
        @param bwPacket: Optional delimiter packet instance
        @return list: Incomplete packets or delimiter control packet"""
        with BoswatchModule._lock:
            orphaned = BoswatchModule._tone_ric_packets[freq].copy()
            BoswatchModule._tone_ric_packets[freq].clear()
            BoswatchModule._last_tone_ric_time.pop(freq, None)
            BoswatchModule._processing_text_ric[freq] = False

        if orphaned:
            age_seconds = time.time() - orphaned[0].get('_multicast_timestamp', time.time())

            logging.debug("[%s] Delimiter RIC=%s cleared %d orphaned tone-RICs on freq %s: RICs=[%s], age=%.1fs → Creating INCOMPLETE multicast packets for forwarding", self.name, ric, len(orphaned), freq, ', '.join([packet.get('ric', 'unknown') for packet in orphaned]), age_seconds)
            return self._create_incomplete_multicast(freq, orphaned)
        if bwPacket is not None:
            self._set_mcast_metadata(bwPacket, "control", "delimiter", ric, "0", "0")
            return [bwPacket]
        return None

# ============================================================
# PACKET METADATA HELPERS
# ============================================================

    def _set_mcast_metadata(self, packet, mode, role, source="", count="1", index="1"):
        r"""!Helper to set standard multicast fields and register wildcards.

        @param packet: The Packet instance to modify
        @param mode: multicastMode (complete, incomplete, single, control)
        @param role: multicastRole (recipient, single, delimiter, netident)
        @param source: The originating RIC
        @param count: Total number of recipients
        @param index: Current recipient index
        @return None"""
        logging.debug(f"Setze Metadata - Mode: {mode}, Role: {role} für RIC: {source}")
        mapping = {
            "multicastMode": (mode, "{MCAST_MODE}"),
            "multicastRole": (role, "{MCAST_ROLE}"),
            "multicastSourceRic": (source, "{MCAST_SOURCE}"),
            "multicastRecipientCount": (str(count), "{MCAST_COUNT}"),
            "multicastRecipientIndex": (str(index), "{MCAST_INDEX}")
        }
        for key, (val, wildcard) in mapping.items():
            packet.set(key, val)
            self._register_wildcard_safe(wildcard, key)

    def _apply_list_tags(self, packet, recipient_dicts):
        r"""!Helper to aggregate fields from all recipients into comma-separated lists.

        @param packet: The target Packet instance
        @param recipient_dicts: List of dictionaries of all recipients in this group
        @return None"""
        all_fields = set()
        for r in recipient_dicts:
            all_fields.update(k for k in r.keys() if not k.startswith('_'))

        for f in sorted(all_fields):
            list_val = ", ".join([str(r.get(f, "")) for r in recipient_dicts])
            list_key = f"{f}_list"
            packet.set(list_key, list_val)
            self._register_wildcard_safe("{" + f.upper() + "_LIST}", list_key)

    def _register_wildcard_safe(self, wildcard, field):
        r"""!Register wildcard if not already globally registered.

        @param wildcard: The wildcard string (e.g. {MCAST_MODE})
        @param field: The packet field name
        @return None"""
        if wildcard not in BoswatchModule._wildcards_registered:
            self.registerWildcard(wildcard, field)
            BoswatchModule._wildcards_registered.add(wildcard)

# ============================================================
# CLEANUP & TIMEOUT MANAGEMENT
# ============================================================

    @staticmethod
    def _global_cleanup_worker():
        r"""!Static background thread that ticks all active module instances.

        @param None
        @return None"""
        logging.info("Global multicast cleanup ticker active")
        while BoswatchModule._running:
            time.sleep(1)
            with BoswatchModule._lock:
                active_instances = BoswatchModule._instances[:]
            for instance in active_instances:
                try:
                    instance._perform_instance_tick()
                except Exception as e:
                    logging.error("Error in instance cleanup: %s", e)
            if int(time.time()) % 60 == 0:
                BoswatchModule._cleanup_hard_timeout_global()

    def _perform_instance_tick(self):
        r"""!Tick-entry point for this specific instance.

        @param None
        @return None"""
        self._check_all_my_frequencies()

    def _check_all_my_frequencies(self):
        r"""!Monitor timeouts for all frequencies assigned to this instance.

        @param None
        @return None"""
        incomplete_packets = []
        trigger_data = []

        with BoswatchModule._lock:
            current_time = time.time()
            for freq in list(self._my_frequencies):
                if freq not in BoswatchModule._tone_ric_packets or not BoswatchModule._tone_ric_packets[freq]:
                    continue

                if BoswatchModule._processing_text_ric.get(freq, False):
                    flag_age = current_time - BoswatchModule._processing_text_ric_started.get(freq, current_time)
                    if flag_age > 2:
                        BoswatchModule._processing_text_ric[freq] = False
                        BoswatchModule._processing_text_ric_started.pop(freq, None)
                    else:
                        continue

                last_time = BoswatchModule._last_tone_ric_time.get(freq, 0)
                if current_time - last_time > self._auto_clear_timeout:
                    recipient_dicts = BoswatchModule._tone_ric_packets[freq].copy()
                    safe_ric = recipient_dicts[0].get('ric', self._DEFAULT_TRIGGER_RIC)
                    trigger_data.append((freq, safe_ric))
                    BoswatchModule._tone_ric_packets[freq].clear()
                    BoswatchModule._last_tone_ric_time.pop(freq, None)

                    logging.info("[%s] Auto-clear: %d tone-RICs on %s (Timeout %ds)", self.name, len(recipient_dicts), freq, self._auto_clear_timeout)
                    packets = self._create_incomplete_multicast(freq, recipient_dicts)
                    if packets:
                        incomplete_packets.extend(packets)

        if incomplete_packets:
            with BoswatchModule._queue_lock:
                BoswatchModule._packet_queue.extend(incomplete_packets)
            for freq, safe_ric in trigger_data:
                self._send_wakeup_trigger(freq, safe_ric)

    def _check_instance_auto_clear(self, freq):
        r"""!Check if frequency has exceeded timeout (called from doWork).

        @param freq: Frequency identifier
        @return list: Incomplete packets if timeout exceeded, else None"""
        with BoswatchModule._lock:
            if freq not in BoswatchModule._tone_ric_packets or not BoswatchModule._tone_ric_packets[freq]:
                return None
            last_time = BoswatchModule._last_tone_ric_time.get(freq, 0)
            if time.time() - last_time > self._auto_clear_timeout:
                recipient_dicts = BoswatchModule._tone_ric_packets[freq].copy()
                BoswatchModule._tone_ric_packets[freq].clear()
                BoswatchModule._last_tone_ric_time.pop(freq, None)
                logging.warning("[%s] Auto-clear (doWork): %d packets", self.name, len(recipient_dicts))
                return self._create_incomplete_multicast(freq, recipient_dicts)
        return None

    @staticmethod
    def _cleanup_hard_timeout_global():
        r"""!Global failsafe for really old packets (ignores instance config).

        @param None
        @return None"""
        with BoswatchModule._lock:
            current_time = time.time()
            max_hard_timeout = 120
            if BoswatchModule._instances:
                max_hard_timeout = max(inst._hard_timeout for inst in BoswatchModule._instances)
            for freq in list(BoswatchModule._tone_ric_packets.keys()):
                BoswatchModule._tone_ric_packets[freq] = [
                    p for p in BoswatchModule._tone_ric_packets[freq]
                    if current_time - p.get('_multicast_timestamp', 0) < max_hard_timeout
                ]
                if not BoswatchModule._tone_ric_packets[freq]:
                    del BoswatchModule._tone_ric_packets[freq]

# ============================================================
# TRIGGER SYSTEM
# ============================================================

    def _send_wakeup_trigger(self, freq, fallback_ric):
        r"""!Send a loopback trigger using the standard TCPClient class."""
        try:
            trigger_ric = self._trigger_ric if self._trigger_ric else fallback_ric
            payload = {
                "timestamp": time.time(),
                "mode": "pocsag",
                "bitrate": "1200",
                "ric": trigger_ric,
                "subric": "1",
                "subricText": "a",
                "message": BoswatchModule._MAGIC_WAKEUP_MSG,
                "clientName": "MulticastTrigger",
                "inputSource": "loopback",
                "frequency": freq
            }
            json_str = json.dumps(payload)

            # using BOSWatch-Architecture
            client = TCPClient(timeout=2)
            if client.connect(self._trigger_host, self._trigger_port):
                # 1. Send
                client.transmit(json_str)

                # 2. Recieve (getting [ack] and prevents connection reset)
                client.receive(timeout=1)

                client.disconnect()
                logging.debug("[%s] Wakeup trigger sent and acknowledged (RIC=%s)", self.name, trigger_ric)
            else:
                logging.error("[%s] Could not connect to local server for wakeup", self.name)

        except Exception as e:
            logging.error("[%s] Failed to send wakeup trigger: %s", self.name, e)

# ============================================================
# LIFECYCLE (End)
# ============================================================

    def onUnload(self):
        r"""!Unregister instance from the global cleanup process.

        @param None
        @return None"""
        with BoswatchModule._lock:
            if self in BoswatchModule._instances:
                BoswatchModule._instances.remove(self)
        logging.debug("[%s] Multicast instance unloaded", self.name)
