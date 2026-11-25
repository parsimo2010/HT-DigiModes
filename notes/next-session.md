# Next session on native Linux

**Start with the installed radio.** The DM-1701 runs the station-specific RadioFoundry build based on `4c6a56e5`. On 425.525 MHz the LibreSDR decoded its link setup, all six numbered M17 data frames and the end flag. All 96 bytes matched. Factory calibration was saved before tuning and verified after the station update. Stock Radioddity V02.03 CSV is the tested recovery image. [First RF capture, measurements and checksums](dm1701-m17-first-rf.md).

The next development target is **LibreSDR transmits a known burst → DM-1701 decodes it**. The present handheld firmware implements the transmit side. Its FM VFO display is expected for this bench build. Handheld M17 reception and Codec2 voice each still need implementation and an on-air demonstration.

## Bring the known reference to Linux

Clone this repository on the native Linux computer and connect both devices directly over USB. Bring the separate **private** archive `HT-DigiModes-Private/native-linux-handoff.zip` from the previous Windows computer. It contains the qualified UHD runtime images, a short raw IQ recording, the personalized vector, expected decoder output, capture helper, installed firmware, stock fallback, codeplug and factory calibration backup. Keep it in operator-controlled storage outside the checkout. The existing Windows and WSL backup copies share one physical computer.

From the checkout, unpack the archive once into a new private directory using Bash:

```bash
umask 077
export KIT="$HOME/ht-m17-private"
mkdir -m 700 "$KIT"
python3 -m zipfile -e "$HOME/Downloads/native-linux-handoff.zip" "$KIT"
(cd "$KIT" && sha256sum -c SHA256SUMS)
export UHD_IMAGES_DIR="$KIT/uhd"
```

On Ubuntu/Debian, the receive and analysis tools use GNU Radio 3.10, UHD, NumPy and SciPy. The build also needs a C++ compiler, CMake and GNU Radio development files. Use the distro Python for its GNU Radio bindings. Install missing packages as needed:

```bash
sudo apt install git build-essential cmake doxygen gnuradio gnuradio-dev uhd-host python3-numpy python3-scipy python3-serial
```

Build gr-m17 at `c6ec482121f964d446fab4e247916b0942f6d4b2` with its submodules using the [Linux build recipe](m17-reference.md#repeat-on-linux) through the environment exports. Use the new machine's Python version and library directory. The previous `~/ht-m17/env.sh` contained WSL installation paths. Keep the exports in the native shell or its own environment file. Reserve the [ARM firmware toolchain](dm1701-build.md) and [RadioFoundry patches](dm1701-m17-ptt.md#repeat-on-the-computer) for work on the handheld receiver.

## First result on the new host

From the lab checkout, replay the captured RF once. This exercises the complete decoder before the USB devices enter the picture.

```bash
python3 scripts/m17_rx.py --iq "$KIT/rf/m17-rf-burst.cf32" --rate 960000 --seconds 2 \
  --carrier-offset-hz=-750 --check-ramp --expect-frames 6
```

Expect six payloads and SHA-256 `6c6b011011c3e8b3086372c9e52bdc83294796bf7b9150ab099e9314052c106f`. For a live repeat, use the qualified B210 image from the kit, USB 3, channel A RX2, 960 ksample/s and 0 dB receive gain. The −750 Hz correction worked for this radio/SDR pair. A new capture can establish the current offset. [SDR qualification](../hardware/libresdr/qualification.md).

The kit includes the receive-only helper used for the successful run. In one terminal, choose a fresh capture name and run:

```bash
run="native-$(date -u +%Y%m%dT%H%M%SZ)"
python3 "$KIT/rf/capture.py" "$run"
```

On an operator-agreed live test, wait for `READY`, then hold SK1 and press PTT for one to two seconds. The firmware sends one bounded burst. Key within the first 20 seconds so the receiver can replay it with the 30-second command below. The helper ends automatically after 90 seconds, or when a second terminal creates `$KIT/rf/<capture-name>.stop`. Back in the first terminal:

```bash
python3 scripts/m17_rx.py --iq "$KIT/rf/$run.cf32" --rate 960000 --seconds 30 \
  --carrier-offset-hz=-750 --check-ramp --expect-frames 6
```

## Make the next on-air test count

Use short, operator-keyed indoor tests at the handheld's low setting with separate stub antennas for functional checks. The operator describes the setup as nominally 1 W and prefers it for these brief tests. The first capture measured received samples, timing and spectrum. Transmitter output in watts and effects outside the house were unmeasured.

Once replay works, move to the reverse direction. Build the handheld receive path against the saved vectors, then send an operator-authorized, finite reference burst from GNU Radio through the LibreSDR. Record how many frames were sent and how many correct payloads **the handheld** produced. A matching link setup and six matching ramp payloads is the first pass. If it fails, use the first missing observation to choose a diagnostic: check radio input samples if no signal arrives, timing and sync if samples arrive, or framing/FEC if sync arrives with bad payloads. Keep the working native transmitter for the subsequent Codec2 voice milestone. The DM-1801 Pro and RADE remain a separate track.
