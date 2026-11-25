# Arrival-day observation log

## 2026-11-24 — DM-1701 host-side USB check

- With the radio off, Windows showed no matching radio entry. After the operator powered it on normally with the cable still attached, Windows listed `Digital Radio in USB mode` with USB VID:PID `0483:DF11`.
- Windows reported Device Manager Code 28 (driver not installed). This confirms enumeration only. The [RadioFoundry hardware reference](https://radiofoundry.org/docs/spec/hardware-dm1701) documents that the stock application and the loader share this USB ID, so the ID alone does not establish which mode is active.
- The check used only Windows Plug and Play inventory and its problem-code property. No radio software opened the device. No codeplug, firmware, or calibration was read or written. No unit-specific identifier is recorded here.
- Radioddity's legacy STTub30 Windows driver package installed but failed to load (Code 39) and was removed. Ubuntu under WSL has qdmr/dmrconf 0.13.3 installed. The radio was not attached to WSL and no backup was attempted through it.

## 2026-11-24 — Operator bench report

- The operator confirmed transmit and receive in both analog FM and DMR on the DM-1701 and DM-1801 Pro. These are functional smoke tests, not instrumented RF measurements.
- The DM-1701 is the active development target. Its normal menu reports firmware `D012.006` and CP version `V01.05`. The operator reported it powered on at its regular screen with native USB attached.
- The second radio is confirmed as a DM-1801 Pro. Its board revision, cable and factory backup status remain unverified.
- No codeplug, installed firmware or calibration had been captured at the time of the bench report.

## DM-1701 stock codeplug backup

- After explicit operator approval, passed the normally booted DM-1701 through to Ubuntu using usbipd-win 5.3.0 and ran `dmrconf --radio dm1701 --bin read` with dmrconf 0.13.3. The read exited successfully. USB sharing was removed afterward.
- The DfuSe binary is 844,093 bytes. dmrconf decoded it offline, and both files have verified SHA-256 hashes in a private manifest. No backup contents or unit-specific identifiers are in Git.
- The file covers two codeplug data ranges, not the installed MCU firmware or factory SPI security registers. The documented working calibration window within the file was all zero, so there is no usable calibration backup from this read. No write, flash, or RF test was run.

## Remaining arrival checklist

- DM-1701 exact marking/FCC ID (private attachment):
- DM-1701 exact vendor recovery package and variant:
- DM-1801 exact marking/FCC ID (private attachment):
- DM-1801 Pro board revision:
- DM-1801 stock firmware version:
- DM-1801 cable type / read-only serial result:
- Second offline copy of the DM-1701 codeplug and private manifest:
- Firmware/codec/calibration backup status (keep artifact paths and hashes in the private manifest):
- Instrumented RF baselines (separate from functional smoke tests):
- LibreSDR UHD model / clock / FPGA image:
- RF load / attenuators / coupler / input limit verified:
- Unresolved blockers:
