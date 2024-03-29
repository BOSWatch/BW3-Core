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

@file:        test_Decoder.py
@date:        15.12.2017
@author:      Bastian Schroll
@description: Unittests for BOSWatch. File have to run as "pytest" unittest
"""
# problem of the pytest fixtures
# pylint: disable=redefined-outer-name
import logging

from boswatch.decoder.decoder import Decoder


def setup_function(function):
    logging.debug("[TEST] %s.%s", function.__module__, function.__name__)


def test_decoderNoData():
    r"""!Test a empty string"""
    assert Decoder.decode("") is None


def test_decoderZveiValid():
    r"""!Test valid ZVEI"""
    assert not Decoder.decode("ZVEI1: 12345") is None
    assert not Decoder.decode("ZVEI1: 12838") is None
    assert not Decoder.decode("ZVEI1: 34675") is None


def test_decoderZveiDoubleTone():
    r"""!Test doubleTone included ZVEI"""
    assert not Decoder.decode("ZVEI1: 6E789") is None
    assert not Decoder.decode("ZVEI1: 975E7") is None
    assert not Decoder.decode("ZVEI1: 2E87E") is None


def test_decoderZveiInvalid():
    """Test invalid ZVEI"""
    assert Decoder.decode("ZVEI1: 1245A") is None
    assert Decoder.decode("ZVEI1: 1245") is None
    assert Decoder.decode("ZVEI1: 135") is None
    assert Decoder.decode("ZVEI1: 54") is None
    assert Decoder.decode("ZVEI1: 54") is None


def test_decoderPocsagValid():
    r"""!Test valid POCSAG"""
    assert not Decoder.decode("POCSAG512: Address: 1000000  Function: 0") is None
    assert not Decoder.decode("POCSAG512: Address: 1000001  Function: 1") is None
    assert not Decoder.decode("POCSAG1200: Address: 1000002  Function: 2") is None
    assert not Decoder.decode("POCSAG2400: Address: 1000003  Function: 3") is None


def test_decoderPocsagText():
    r"""!Test POCSAG with text"""
    assert not Decoder.decode("POCSAG512: Address: 1000000  Function: 0  Alpha:   test") is None
    assert not Decoder.decode("POCSAG512: Address: 1000001  Function: 1  Alpha:   test") is None
    assert not Decoder.decode("POCSAG1200: Address: 1000002  Function: 2  Alpha:   test") is None
    assert not Decoder.decode("POCSAG2400: Address: 1000003  Function: 3  Alpha:   test") is None


def test_decoderPocsagShortRic():
    r"""!Test short POCSAG"""
    assert not Decoder.decode("POCSAG512: Address:       3  Function: 0  Alpha:   test") is None
    assert not Decoder.decode("POCSAG512: Address:      33  Function: 0  Alpha:   test") is None
    assert not Decoder.decode("POCSAG1200: Address:     333  Function: 0  Alpha:   test") is None
    assert not Decoder.decode("POCSAG1200: Address:    3333  Function: 0  Alpha:   test") is None
    assert not Decoder.decode("POCSAG2400: Address:   33333  Function: 0  Alpha:   test") is None
    assert not Decoder.decode("POCSAG2400: Address:  333333  Function: 0  Alpha:   test") is None
    assert not Decoder.decode("POCSAG2400: Address: 3333333  Function: 0  Alpha:   test") is None


def test_decoderPocsagInvalid():
    r"""!Test invalid POCSAG"""
    assert Decoder.decode("POCSAG512: Address: 333333F  Function: 0  Alpha:   invalid") is None
    assert Decoder.decode("POCSAG512: Address: 333333F  Function: 1  Alpha:   invalid") is None
    assert Decoder.decode("POCSAG512: Address: 3333333  Function: 4  Alpha:   invalid") is None


def test_decoderFmsValid():
    r"""!Test valid FMS"""
    assert not Decoder.decode("""FMS: 43f314170000 (9=Rotkreuz       3=Bayern 1         Ort 0x25=037FZG  7141Status  3=Einsatz Ab     0=FZG->LST 2=I  (ohneNA,ohneSIGNAL)) CRC correct""") is None
    assert not Decoder.decode("""FMS: 43f314170000 (9=Rotkreuz       3=Bayern 1         Ort 0x25=037FZG  7141Status  3=Einsatz Ab     1=LST->FZG 2=I  (ohneNA,ohneSIGNAL)) CRC correct""") is None
    assert not Decoder.decode("""FMS: 43f314170000 (9=Rotkreuz       3=Bayern 1         Ort 0x25=037FZG  7141Status  3=Einsatz Ab     0=FZG->LST 2=II (ohneNA,mit SIGNAL)) CRC correct""") is None
    assert not Decoder.decode("""FMS: 43f314170000 (9=Rotkreuz       3=Bayern 1         Ort 0x25=037FZG  7141Status  3=Einsatz Ab     1=LST->FZG 2=III(mit NA,ohneSIGNAL)) CRC correct""") is None
    assert not Decoder.decode("""FMS: 43f314170000 (9=Rotkreuz       3=Bayern 1         Ort 0x25=037FZG  7141Status  3=Einsatz Ab     0=FZG->LST 2=IV (mit NA,mit SIGNAL)) CRC correct""") is None


def test_decoderFmsInvalid():
    r"""!Test invalid FMS"""
    assert Decoder.decode("""FMS: 14170000 (9=Rotkreuz       3=Bayern 1         Ort 0x25=037FZG  7141Status  3=Einsatz Ab     1=LST->FZG 2=III(mit NA,ohneSIGNAL)) CRC correct""") is None
    assert Decoder.decode("""FMS: 43f314170000 (9=Rotkreuz       3=Bayern 1         Ort 0x25=037FZG  7141Sta  3=Einsatz Ab     0=FZG->LST 2=IV (mit NA,mit SIGNAL)) CRC correct""") is None
    assert Decoder.decode("""FMS: 14170000 (9=Rotkreuz       3=Bayern 1         Ort 0x25=037FZG  7141Status  3=Einsatz Ab     1=LST->FZG 2=III(mit NA,ohneSIGNAL)) CRC incorrect""") is None
    assert Decoder.decode("""FMS: 43f314170000 (9=Rotkreuz       3=Bayern 1         Ort 0x25=037FZG  7141Sta  3=Einsatz Ab     0=FZG->LST 2=IV (mit NA,mit SIGNAL)) CRC incorrect""") is None
