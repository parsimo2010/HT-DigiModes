# LAB-004 and M17-001 | 2026-11-24

**Computer loopback passed.** The clean reference decoder received AB1CDE to AB2CDE, type 0003, no encryption, CAN 0. Frame 0000 contained `00000000 00000000 00010203 04050600` with decoder metric `e=0.0`. All 82 complete 16-byte outputs matched the repeating source. The example starts its data source before the start button, so the byte rotation and number of frames in a timed run can vary. An initial attempt to press Start before starting the graph produced zero frames. The runner presses it after startup and checks the decoded bytes.

The fixture records the actual encoder output at the symbol port. After the 192-symbol preamble come the link setup frame and stream frame 0000, each 192 symbols (40 ms at 4800 symbols/s). The bits are the inverse symbol mapping, MSB first, including sync, FEC and randomization. For an independent replay we fed the captured preamble pattern, these two symbol vectors, the end marker and zero padding into a fresh pinned GNU Radio decoder. It returned exactly the 16 bytes above. These are synthetic upstream example addresses.

A second run used the example's full pulse shaping, FM, simulated noisy channel, demodulator and symbol synchronizer. We set noise voltage to 0.01 and replaced the repeated zeros with bytes 00 through 0F to expose payload errors. FN 0000 through 0050 returned 81 matching payloads, zero erroneous bits in 10,368 decoded payload bits. FN 0000 had e=3.5. The graph stopped while buffers still contained frames. This count covers decoded output only. The fractional decoder metric is distinct from measured bit errors.

| Saved artifact | SHA-256 |
|---|---|
| [Frame bits and symbols](../tests/vectors/m17-loopback.json), LF serialization | `a54dd2308832c5cebf8c228b9a38a0df7c1f1f901afcca584019364e94ac9797` |
| Clean decoded.bin, 1,312 bytes | `c0518725e41c262a01942ebd66fb9eff275ccf702cb9804bba13e3586c58372d` |
| Noisy channel output noisy.cf32, 162,552 little-endian complex float32 samples | `7d7aec2bcbf2bc9e1240ee67da272fe05f2910b6c2404aeb639209faf2f9a53e` |

Binary captures are in Ubuntu WSL under `~/ht-m17/graphs/`. [Simulation settings](m17-channel.json) and the [spectrum of that capture](m17-simulated-spectrum.png) describe the software channel. Spectrum uses Welch averaging, a 1024-sample Hann window, 50% overlap and peak-normalized power density.

## Repeat on Linux

Tested on Ubuntu 26.04 x86_64 (WSL2), GNU Radio 3.10.12.0-6, Python 3.14.4, GCC/G++ 15.2.0, CMake 4.2.3, GNU Make 4.4.1. Install `git cmake build-essential doxygen gnuradio gnuradio-dev` using apt. Run from the lab checkout. Use a fresh output directory for each run.

```bash
set -eu
labdir=$PWD
mkdir -p ~/ht-m17
cd ~/ht-m17
git clone https://github.com/M17-Project/gr-m17
git -C gr-m17 checkout --detach c6ec482121f964d446fab4e247916b0942f6d4b2
git -C gr-m17 submodule update --init --recursive
git -C gr-m17 submodule status --recursive
cmake -S gr-m17 -B gr-m17/build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$PWD/prefix"
cmake --build gr-m17/build -j6
cmake --install gr-m17/build
export LD_LIBRARY_PATH="$PWD/prefix/lib/$(gcc -dumpmachine)"
export PYTHONPATH="$PWD/prefix/lib/python$(python3 -c 'import sys; print("%s.%s" % sys.version_info[:2])')/site-packages"
export GRC_BLOCKS_PATH="$PWD/prefix/share/gnuradio/grc/blocks"
export QT_QPA_PLATFORM=offscreen
out=$(mktemp -d "$PWD/graphs.XXXXXX")
grcc -o "$out" gr-m17/examples/m17_loopback.grc
grcc -o "$out" gr-m17/examples/m17_loopback_noisychannel.grc
cd "$out"
sed -i "s|'/tmp/dump.bin'|'decoded.bin'|" m17_loopback.py
PYTHONPATH="$PWD:$PYTHONPATH" timeout 25 python3 "$labdir/scripts/m17_reference.py" > run.log 2>&1
tail -2 run.log
sha256sum reference.json decoded.bin noisy.cf32
```

Both generated graphs have only host endpoints. The runner adds data taps and uses the example start/end messages in-process. It does not load an SDR graph. The GNU Radio reference and its GPL dependencies stay in the external checkout. The host framing implementation derives from the [M17 protocol specification](https://spec.m17project.org/files/M17_spec.pdf), sections 1–2 and appendices B–F. Run `python3 -m unittest discover -s tests -v` from the lab root to compare it with the saved vectors without GNU Radio. NOT RUN ON HARDWARE.
