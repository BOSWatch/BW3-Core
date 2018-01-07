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

@file:        test_decoder.py
@date:        15.12.2017
@author:      Bastian Schroll
@description: Unittests for BOSWatch. File must be run as "pytest" unittest
"""

from boswatch.decoder import decoder


class Test_decoder:
    """!Unittests for the decoder"""

    def test_decoder_no_data(self):
        """!Test a empty string"""
        assert decoder.getDecoder("").decode("") is None

    def test_decoder_zvei_valid(self):
        """!Test valid ZVEI"""
        dec = decoder.getDecoder("ZVEI")
        assert not dec.decode("ZVEI1: 12345") is None
        assert not dec.decode("ZVEI1: 12838") is None
        assert not dec.decode("ZVEI1: 34675") is None

    def test_decoder_zvei_doubleTone(self):
        """!Test doubleTone included ZVEI"""
        dec = decoder.getDecoder("ZVEI")
        assert not dec.decode("ZVEI1: 6E789") is None
        assert not dec.decode("ZVEI1: 975E7") is None
        assert not dec.decode("ZVEI1: 2E87E") is None

    def test_decoder_zvei_invalid(self):
        """Test invalid ZVEI"""
        dec = decoder.getDecoder("ZVEI")
        assert dec.decode("ZVEI1: 1245A") is None
        assert dec.decode("ZVEI1: 1245") is None
        assert dec.decode("ZVEI1: 135") is None
        assert dec.decode("ZVEI1: 54") is None
        assert dec.decode("ZVEI1: 54") is None

    def test_decoder_pocsag_valid(self):
        """!Test valid POCSAG"""
        dec = decoder.getDecoder("POCSAG")
        assert not dec.decode("POCSAG512: Address: 1000000  Function: 0") is None
        assert not dec.decode("POCSAG512: Address: 1000001  Function: 1") is None
        assert not dec.decode("POCSAG1200: Address: 1000002  Function: 2") is None
        assert not dec.decode("POCSAG2400: Address: 1000003  Function: 3") is None

    def test_decoder_pocsag_text(self):
        """!Test POCSAG with text"""
        dec = decoder.getDecoder("POCSAG")
        assert not dec.decode("POCSAG512: Address: 1000000  Function: 0  Alpha:   test") is None
        assert not dec.decode("POCSAG512: Address: 1000001  Function: 1  Alpha:   test") is None
        assert not dec.decode("POCSAG1200: Address: 1000002  Function: 2  Alpha:   test") is None
        assert not dec.decode("POCSAG2400: Address: 1000003  Function: 3  Alpha:   test") is None

    def test_decoder_pocsag_short(self):
        """!Test short POCSAG"""
        dec = decoder.getDecoder("POCSAG")
        assert not dec.decode("POCSAG512: Address:       3  Function: 0  Alpha:   test") is None
        assert not dec.decode("POCSAG512: Address:      33  Function: 0  Alpha:   test") is None
        assert not dec.decode("POCSAG1200: Address:     333  Function: 0  Alpha:   test") is None
        assert not dec.decode("POCSAG1200: Address:    3333  Function: 0  Alpha:   test") is None
        assert not dec.decode("POCSAG2400: Address:   33333  Function: 0  Alpha:   test") is None
        assert not dec.decode("POCSAG2400: Address:  333333  Function: 0  Alpha:   test") is None
        assert not dec.decode("POCSAG2400: Address: 3333333  Function: 0  Alpha:   test") is None

    def test_decoder_pocsag_invalid(self):
        """!Test invalid POCSAG"""
        dec = decoder.getDecoder("POCSAG")
        assert dec.decode("POCSAG512: Address: 333333F  Function: 0  Alpha:   invalid") is None
        assert dec.decode("POCSAG512: Address: 333333F  Function: 1  Alpha:   invalid") is None
        assert dec.decode("POCSAG512: Address: 3333333  Function: 4  Alpha:   invalid") is None

    def test_decoder_fms_valid(self):
        """!Test valid FMS"""
        dec = decoder.getDecoder("FMS")
        assert not dec.decode("""FMS: 43f314170000 (9=Rotkreuz       3=Bayern 1         Ort 0x25=037FZG  7141Status  3=Einsatz Ab     0=FZG->LST 2=I  (ohneNA,ohneSIGNAL)) CRC correct""") is None
        assert not dec.decode("""FMS: 43f314170000 (9=Rotkreuz       3=Bayern 1         Ort 0x25=037FZG  7141Status  3=Einsatz Ab     1=LST->FZG 2=I  (ohneNA,ohneSIGNAL)) CRC correct""") is None
        assert not dec.decode("""FMS: 43f314170000 (9=Rotkreuz       3=Bayern 1         Ort 0x25=037FZG  7141Status  3=Einsatz Ab     0=FZG->LST 2=II (ohneNA,mit SIGNAL)) CRC correct""") is None
        assert not dec.decode("""FMS: 43f314170000 (9=Rotkreuz       3=Bayern 1         Ort 0x25=037FZG  7141Status  3=Einsatz Ab     1=LST->FZG 2=III(mit NA,ohneSIGNAL)) CRC correct""") is None
        assert not dec.decode("""FMS: 43f314170000 (9=Rotkreuz       3=Bayern 1         Ort 0x25=037FZG  7141Status  3=Einsatz Ab     0=FZG->LST 2=IV (mit NA,mit SIGNAL)) CRC correct""") is None

    def test_decoder_fms_invalid(self):
        """!Test invalid FMS"""
        dec = decoder.getDecoder("FMS")
        assert dec.decode("""FMS: 14170000 (9=Rotkreuz       3=Bayern 1         Ort 0x25=037FZG  7141Status  3=Einsatz Ab     1=LST->FZG 2=III(mit NA,ohneSIGNAL)) CRC correct""") is None
        assert dec.decode("""FMS: 43f314170000 (9=Rotkreuz       3=Bayern 1         Ort 0x25=037FZG  7141Sta  3=Einsatz Ab     0=FZG->LST 2=IV (mit NA,mit SIGNAL)) CRC correct""") is None
        assert dec.decode("""FMS: 14170000 (9=Rotkreuz       3=Bayern 1         Ort 0x25=037FZG  7141Status  3=Einsatz Ab     1=LST->FZG 2=III(mit NA,ohneSIGNAL)) CRC incorrect""") is None
        assert dec.decode("""FMS: 43f314170000 (9=Rotkreuz       3=Bayern 1         Ort 0x25=037FZG  7141Sta  3=Einsatz Ab     0=FZG->LST 2=IV (mit NA,mit SIGNAL)) CRC incorrect""") is None
