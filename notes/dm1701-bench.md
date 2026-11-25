# DM-1701 bench handoff | HOLD | 2026-11-24

The operator reports normal operation on Radioddity V02.03 CSV, menu V002.003. The USB update route and this stock fallback were tested. D012.006 was never dumped. Keep the existing private channel backup. Channel migration is optional. Factory calibration still needs a private readback. No approval is pending for a flash or transmission.

## Offline preview of the built image

Ran this from the pinned RadioFoundry tree without a key, USB connection or device discovery. The writer validated model and image, then reported the following plan for the plain LAB-009 image with SHA-256 `a1930d2b91248f04952553997fe9d5511860f5d237dec383c96fd7df77f017cd`.

```bash
python3 tools/stm32_dfu.py --model dm1701 --dry-run build/dm1701/rfoundry_dm1701.bin
```

All endpoints below are exclusive.

| MCU sector | Erase from | Erase to | Planned 1 KiB write blocks |
|---|---|---|---:|
| 3 | 0x0800C000 | 0x08010000 | 16 |
| 4 | 0x08010000 | 0x08020000 | 64 |
| 5 | 0x08020000 | 0x08040000 | 128 |
| 6 | 0x08040000 | 0x08060000 | 128 |
| 7 | 0x08060000 | 0x08080000 | 128 |
| 8 | 0x08080000 | 0x080A0000 | 128 |
| 9 | 0x080A0000 | 0x080C0000 | 99 |
| 10 | 0x080C0000 | 0x080E0000 | 0 |
| 11 | 0x080E0000 | 0x08100000 | 0 |

The image ends at 0x080B89BC. Padding extends the programmed range to 0x080B8C00 (691 blocks, 707,584 bytes). The rest through 0x08100000 would be erased. In particular this would remove stock codec content and leave sectors 10–11 blank. The bootloader occupies 0x08000000–0x0800BFFF. The exit operation sets its address and issues a zero-length reset request. It writes no bootloader data. The updater plan has no external SPI operation, including the factory calibration and flags in the separate security registers. This preview covers the updater only. First boot runs application code.

For any actual candidate, repeat the preview on the final file with the intended writer, including any private codec merge. Bind the image hash, model, exact command and tool revision to the sector list, padded write range and protected regions. Review against the unit's loader descriptor, confirmed stock fallback and private recovery copies before asking the operator for that specific action. The previous stock-update approval is spent.

## First bench session

1. **LAB-003 host setup complete, device setup open.** Ubuntu WSL has UHD 4.9.0.1-1ubuntu1 and both inventory tools. After identifying the exact LibreSDR and host connection, use the separate approval steps in [LibreSDR inventory](../docs/libresdr-inventory.md). Record board and input port, current FPGA image/version, clock, RX rates and probe result privately. Leave the working image in place.
2. **LAB-006 fixture open.** With power off, identify a 50-ohm load rated above worst-case radio output at the test frequency and duty cycle. Route the radio into the directional coupler's input, through port to the load, forward coupled port through a rated pad to the SDR RX, and terminate any unused isolated port as specified. Record models, orientation, loss tolerances and power ratings of each component. Verify the coupled level with a suitable meter and the SDR disconnected before admitting RF to the SDR. Any keyed check needs its own approval.
3. Calculate `P_rx,max (dBm) = 10 log10(1000 × P_tx,max in watts) − minimum coupling loss − minimum pad loss − other verified minimum losses`. Use the actual maximum including tolerance and credit zero for unverified cable losses. Nominal 5 W alone is +37.0 dBm. Record the board/port limit, chosen margin and resulting headroom. Both the worst-case input and the meter reading with uncertainty must be below the limit by that margin. The 5 W figure is a planning value. Load rating, actual isolation, pad ratings, input limit and headroom remain unverified.
4. **LAB-007 stock baseline open.** Once containment and SDR receive setup pass, first prepare a receive-only capture. Obtain separate approval for one bounded stock transmission into the load. Record FM frequency/deviation and, in its own capture, DMR timing, sample settings and private file checksums using the [capture template](../templates/capture-metadata.example.yaml). The earlier smoke tests established basic operation only.
5. **LAB-008 first boot and calibration open.** After a separately approved install, leave settings alone and keep PTT idle. The pinned board registry declares full backup under RadioFoundry. Its calibration loader can read the 512 factory bytes from security registers 1 and 2 and convert them in RAM. Confirm the actual running build and separately authorize the exact read-only backup operation. Save the backup outside Git. Check the bundle manifest, complete `security-registers.bin` (three 256-byte registers including factory flags), matching SHA-256 and a second offline copy. Confirm the two factory register reads are complete, plausible and repeatable. A working table in SPI at 0x010000 or a codeplug export cannot establish that. If unavailable, partial, blank or inconsistent, stop before changing settings or testing RF. Source references at the build pin are `boards/dm1701/board.toml`, `boards/uv380_family/calibration_uvf.c` and `site/static/js/flasher/backup.js`.

The plan also lists LAB-005 as a P0 gate before replacement firmware or developer RF. Its RADE measurement belongs to the separate track and remains open. A first experimental M17 RF test additionally requires a bounded, default-off transmit path and verified timeout/unkey behavior. The present baseline has no M17 transmitter. DM-1801 Pro board and cable identification remain separate.

NOT RUN ON HARDWARE.
