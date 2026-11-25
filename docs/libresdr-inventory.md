# LibreSDR host inventory

Use Python 3.8+ from the checkout root to check local tool availability without touching hardware.

```bash
python3 scripts/lab.py status
python3 -m unittest discover -s tests -v
```

The only subprocesses the status command can launch are the UHD and GNU Radio version tools. On a fresh Debian or Ubuntu SDR host, the distro packages to evaluate for this setup are `python3`, `uhd-host` and `gnuradio`. Record the OS and the exact package versions you used with `dpkg-query -W python3 uhd-host gnuradio`.

## Manual device checks

The two examples below are **not** run by the lab CLI or tests. Use them separately only after agreeing on the exact SDR, command and safety checks. Discovery contacts devices and probing can initialize the SDR. These examples do not request TX, flashing or image updates. Do not load a stock USRP image onto a LibreSDR to try to make it appear.

Use a verified address for the unit and keep stdout/stderr outside the checkout. The shell variables below must point to your own device address and an existing private output directory.

```bash
uhd_find_devices --args="addr=${LIBRESDR_ADDR:?Set the verified SDR address}" > "${LAB_PRIVATE_DIR:?Set a private directory}/uhd-find.txt" 2>&1
uhd_usrp_probe --args="addr=${LIBRESDR_ADDR:?Set the verified SDR address}" > "${LAB_PRIVATE_DIR:?Set a private directory}/uhd-probe.txt" 2>&1
```

If discovery fails, stop before probing. Keep the exact command, exit code and log privately. Share only a sanitized model, UHD version, FPGA image version or local image SHA-256, and any error without serials or addresses. UHD compatibility is not yet verified.

## M17 receiver on the computer

The GNU Radio flow in [m17_rx.py](../scripts/m17_rx.py) accepts centered complex float32 I/Q at 48 or 960 ksample/s. It filters the channel to 48 ksample/s, demodulates FM, applies a matched filter and recovers timing before handing symbols to the pinned gr-m17 decoder. Live input uses a single UHD receive channel. The sample limit defaults to five seconds. Use an outer timeout for a disconnected or stalled device.

On Ubuntu, use [the LAB-004 GNU Radio environment and noisy-channel capture](../notes/m17-reference.md). From the lab checkout:

```bash
source ~/ht-m17/env.sh
python3 scripts/m17_rx.py --iq ~/ht-m17/graphs/noisy.cf32 --check-ramp
```

Tested 2026-11-25 with GNU Radio 3.10.12.0 and the capture with SHA-256 `7d7aec2bcbf2bc9e1240ee67da272fe05f2910b6c2404aeb639209faf2f9a53e`. Both the native file and a 960 ksample/s version generated with SciPy `resample_poly(x, 20, 1)` decoded 82 complete 16-byte ramp payloads, SHA-256 `8b92593b24f0a6ab5bd3f24be8530e0bd7f0270da7e288ae825368a14b0f712a`. Counts are for file replay through this receiver. A live M17 decode requires a signal on the verified receive port at the chosen frequency.
