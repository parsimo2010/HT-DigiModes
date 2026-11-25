"""Capture the two pinned, computer-only gr-m17 example graphs (see notes/m17-reference.md)."""
import json
from pathlib import Path
import time

from gnuradio import blocks, gr
from PyQt5 import Qt

from m17_loopback import m17_loopback
from m17_block import m17_block


def frame(symbols, sync):
    if len(symbols) != 192:
        raise ValueError("Incomplete encoder frame")
    mapping = {1: "00", 3: "01", -1: "10", -3: "11"}
    bits = "".join(mapping[symbol] for symbol in symbols)
    if int(bits[:16], 2) != sync:
        raise ValueError("Unexpected frame sync")
    return {"bits": bits, "symbols": list(map(int, symbols))}


def clean_loopback():
    graph = m17_loopback()
    symbols = blocks.vector_sink_f()
    graph.connect(graph.m17_m17_coder_0, symbols)
    graph.start()
    try:
        time.sleep(0.1)
        graph.start_of_transmission.click()
        time.sleep(2.5)
        graph.end_of_transmission.click()
        time.sleep(2)
    finally:
        graph.stop()
        graph.wait()
        graph.blocks_file_sink_0.close()

    payload = Path("decoded.bin").read_bytes()
    pattern = bytes.fromhex("010203040506") + bytes(10)
    first = payload[:16]
    if len(first) != 16 or first not in pattern * 2 or payload != first * (len(payload) // 16):
        raise ValueError("Decoder output differs from the repeated example payload")
    data = symbols.data()
    vector = {
        "source": "AB1CDE", "destination": "AB2CDE", "type": 3,
        "first_payload_hex": first.hex(),
        "link_setup": frame(data[192:384], 0x55F7),
        "stream_0000": frame(data[384:576], 0xFF5D),
    }
    Path("reference.json").write_text(json.dumps(vector, indent=2) + "\n")
    print(f"Clean loopback: {len(payload) // 16} complete payloads matched")


def noisy_loopback():
    graph = m17_block()
    graph.set_noise(0.01)
    graph.blocks_vector_source_x_0.set_data(list(range(16)), [])
    payload = blocks.vector_sink_b()
    iq = blocks.file_sink(gr.sizeof_gr_complex, "noisy.cf32")
    graph.connect(graph.m17_m17_decoder_0, payload)
    graph.connect(graph.channels_channel_model_0, iq)
    graph.start()
    try:
        time.sleep(5)
    finally:
        graph.stop()
        graph.wait()
        iq.close()
    data = bytes(payload.data())
    if not data or data != bytes(range(16)) * (len(data) // 16):
        raise ValueError("Noisy channel payload mismatch or missing output")
    print(f"Noisy channel: {len(data) // 16} complete payloads matched")


if __name__ == "__main__":
    app = Qt.QApplication([])
    clean_loopback()
    noisy_loopback()
