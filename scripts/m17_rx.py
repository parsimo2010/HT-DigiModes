"""Receive an M17 stream from a centered complex float32 recording or a UHD RX port."""
import argparse
import hashlib
import math
import os
from pathlib import Path

from gnuradio import analog, blocks, digital, filter, gr, m17
from gnuradio.filter import firdes


def receive(source, rate, seconds, capture=None):
    graph = gr.top_block("M17 receive test")
    limit = blocks.head(gr.sizeof_gr_complex, int(rate * seconds))
    graph.connect(source, limit)
    decimation = rate // 48000
    channel = filter.fir_filter_ccf(decimation, firdes.low_pass(1, rate, 8500, 3500))
    fm = analog.quadrature_demod_cf(48000 / (2 * math.pi * 800))
    matched = filter.fir_filter_fff(1, firdes.root_raised_cosine(1, 10, 1, 0.5, 81))
    timing = digital.symbol_sync_ff(
        digital.TED_GARDNER, 10, 2 * math.pi * 0.0015, 1, 1, 0.05, 1,
        digital.constellation_bpsk().base(), digital.IR_MMSE_8TAP, 128, [],
    )
    decoder = m17.m17_decoder(True, False, 2.0, 30.0, False, False, 0, "", "", "", 0)
    sink = blocks.vector_sink_b()
    graph.connect(limit, channel, fm, matched, timing, decoder, sink)
    if capture is not None:
        # The sink owns the descriptor. Preserve prior captures and keep new ones private.
        fd = os.open(capture, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        graph.connect(limit, blocks.file_descriptor_sink(gr.sizeof_gr_complex, fd))
    graph.run()
    return bytes(sink.data())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sources = parser.add_mutually_exclusive_group(required=True)
    sources.add_argument("--iq", type=Path, help="little-endian complex float32 file")
    sources.add_argument("--sdr-args", help="UHD device address including qualified FPGA path")
    parser.add_argument("--rate", type=int, choices=(48000, 960000), default=48000)
    parser.add_argument("--seconds", type=int, choices=range(1, 31), default=5, metavar="1..30")
    parser.add_argument("--frequency-hz", type=int)
    parser.add_argument("--antenna", help="verified channel 0 receive port")
    parser.add_argument("--check-ramp", action="store_true", help="expect the lab fixture's 00..0f payload")
    parser.add_argument("--expect-frames", type=int, help="require this exact number of complete payloads")
    parser.add_argument("--capture-iq", type=Path, help="save the limited input to a new private complex float32 file")
    args = parser.parse_args()
    if args.expect_frames is not None and args.expect_frames <= 0:
        parser.error("--expect-frames must be positive")
    if args.iq is not None:
        if args.antenna or args.frequency_hz is not None:
            parser.error("tuning options require --sdr-args")
        if args.iq.stat().st_size % 8:
            parser.error("partial complex sample at end of file")
        source = blocks.file_source(gr.sizeof_gr_complex, str(args.iq), False)
    else:
        if args.rate != 960000 or not args.antenna or not args.frequency_hz or args.frequency_hz <= 0:
            parser.error("live RX requires --rate 960000, --antenna, and a positive --frequency-hz")
        from gnuradio import uhd
        source = uhd.usrp_source(args.sdr_args, uhd.stream_args(cpu_format="fc32", channels=[0]))
        source.set_samp_rate(args.rate)
        if abs(source.get_samp_rate() - args.rate) > 1:
            raise RuntimeError("UHD could not set the requested receive rate")
        source.set_antenna(args.antenna, 0)
        source.set_center_freq(args.frequency_hz, 0)

    payload = receive(source, args.rate, args.seconds, args.capture_iq)
    if not payload or len(payload) % 16:
        raise SystemExit("No complete M17 stream or partial payload output")
    frames = len(payload) // 16
    if args.expect_frames is not None and frames != args.expect_frames:
        raise SystemExit(f"Expected {args.expect_frames} complete payloads, decoded {frames}")
    if args.check_ramp and payload != bytes(range(16)) * frames:
        raise SystemExit("Decoded data differs from the expected ramp")
    print(f"{frames} complete payloads, SHA-256 {hashlib.sha256(payload).hexdigest()}")


if __name__ == "__main__":
    main()
