"""Verify an exact DM-1701 bench image against the mock modem and GNU Radio. No devices."""
import argparse
import hashlib
from pathlib import Path
import subprocess

import numpy as np
from gnuradio import blocks
from gnuradio.filter import firdes
from scipy.signal import upfirdn

from m17_rx import receive


def image_vector(image, elf):
    records = subprocess.check_output(["arm-none-eabi-nm", "-S", elf], text=True)
    for record in records.splitlines():
        fields = record.split()
        if len(fields) == 4 and fields[-1] == "m17_test_burst":
            address, length = (int(field, 16) for field in fields[:2])
            start = address - 0x0800c000
            if length != 432 or start < 0 or start + length > len(image):
                raise ValueError("M17 vector lies outside the expected image or has the wrong length")
            return image[start:start + length]
    raise ValueError("Missing M17 transmit vector in companion ELF")


def simulate(vector, rolloff):
    # Exactly 200 samples/symbol at the qualified SDR input rate. Idle carrier
    # before and after the burst lets the receiver settle and drain its filters.
    levels = (1, 3, -1, -3)
    symbols = [levels[(byte >> shift) & 3] for byte in vector for shift in (6, 4, 2, 0)]
    sps = 200
    taps = firdes.root_raised_cosine(sps, sps, 1, rolloff, 12 * sps + 1)
    pulse = upfirdn(taps, np.r_[np.zeros(960), symbols, np.zeros(1920)], up=sps)
    return np.exp(2j * np.pi * 800 / 960000 * np.cumsum(pulse)).astype(np.complex64)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path)
    parser.add_argument("elf", type=Path)
    parser.add_argument("modem_capture", type=Path, help="output of radioCoreTestM17 --capture")
    args = parser.parse_args()
    vector = image_vector(args.image.read_bytes(), args.elf)
    if vector != args.modem_capture.read_bytes():
        raise ValueError("Final image bytes differ from the actual chunks queued by host PTT")
    print(f"432 bytes across 12 modem chunks, SHA-256 {hashlib.sha256(vector).hexdigest()}")
    for rolloff in (0.5, 0.2):
        signal = simulate(vector, rolloff)
        payload = receive(blocks.vector_source_c(signal, False), 960000, 1)
        if payload != bytes(range(16)) * 6:
            raise ValueError(f"Unexpected stream at simulated RRC roll-off {rolloff}")
        print(f"RRC {rolloff}, 6 payloads, SHA-256 {hashlib.sha256(payload).hexdigest()}")


if __name__ == "__main__":
    main()
