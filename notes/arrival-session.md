# Arrival-day observation log

## 2026-11-24 — DM-1701 host-side USB check

- With the radio off, Windows showed no matching radio entry. After the operator powered it on normally with the cable still attached, Windows listed `Digital Radio in USB mode` with USB VID:PID `0483:DF11`.
- Windows reported Device Manager Code 28 (driver not installed). This confirms enumeration only. The [RadioFoundry hardware reference](https://radiofoundry.org/docs/spec/hardware-dm1701) documents that the stock application and the loader share this USB ID, so the ID alone does not establish which mode is active.
- The check used only Windows Plug and Play inventory and its problem-code property. No radio software opened the device. No codeplug, firmware, or calibration was read or written. No unit-specific identifier is recorded here.
- Radioddity's legacy STTub30 Windows driver package installed but failed to load (Code 39) and was removed. Ubuntu under WSL has qdmr/dmrconf 0.13.3 installed. The radio was not attached to WSL and no backup was attempted through it.

## Remaining arrival checklist

- DM-1701 exact marking/FCC ID (private attachment):
- DM-1701 stock firmware version:
- DM-1701 programming cable and USB ID:
- DM-1801 exact marking/FCC ID (private attachment):
- DM-1801 architecture decision (current HR_C7000 / original v1 / unknown): UNKNOWN
- DM-1801 stock firmware version:
- DM-1801 cable type / read-only serial result:
- Factory codeplug backup status (keep artifact paths and hashes in the private manifest):
- Firmware/codec/calibration backup status (keep artifact paths and hashes in the private manifest):
- Stock FM/DMR results:
- LibreSDR UHD model / clock / FPGA image:
- RF load / attenuators / coupler / input limit verified:
- Unresolved blockers:
