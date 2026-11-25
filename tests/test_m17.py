import json
from pathlib import Path
import unittest

from src.modems import m17


class M17FrameTests(unittest.TestCase):
    vector = json.loads((Path(__file__).parent / "vectors/m17-loopback.json").read_text())
    # AB2CDE, AB1CDE in M17 base 40, plain data stream, empty META.
    link_data = bytes.fromhex("00001f246391 00001f245d51 0003") + bytes(14)

    def check_frame(self, actual, name):
        expected = self.vector[name]
        self.assertEqual("".join(map(str, actual)), expected["bits"])
        self.assertEqual(m17.symbols(actual), expected["symbols"])

    def test_link_setup(self):
        self.check_frame(m17.link_setup_bits(self.link_data), "link_setup")

    def test_first_stream_frame(self):
        payload = bytes.fromhex(self.vector["first_payload_hex"])
        self.check_frame(m17.stream_bits(self.link_data[:5], 0, 0, payload), "stream_0000")

    def test_crc_specification_examples(self):
        self.assertEqual(m17.crc16(b"123456789"), 0x772b)
        self.assertEqual(m17.crc16(bytes(range(256))), 0x1c31)

    def test_frame_lengths_and_fragment_bounds(self):
        with self.assertRaises(ValueError):
            m17.link_setup_bits(bytes(30))
        with self.assertRaises(ValueError):
            m17.stream_bits(bytes(5), 6, 0, bytes(16))
        with self.assertRaises(ValueError):
            m17.symbols([0] * 383)
