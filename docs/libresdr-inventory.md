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
