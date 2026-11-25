# Safety/recovery gates

The operator confirmed basic FM/DMR operation before any change and separately approved the DM-1701 codeplug read and the one Radioddity V02.03 CSV application write recorded in the arrival log. Those approvals do not carry over to a future write or RF operation. For every hardware operation, record:

| Gate | DM-1701 | DM-1801 | Evidence / date / approval |
|---|---|---|---|
| Exact model and interface verified | USB/DFU VERIFIED | PRO IDENTIFIED | DM-1701 native USB and factory update mode were used successfully. Board revisions and DM-1801 Pro cable remain unverified |
| Stock codeplug saved and hash recorded | PASS | OPEN | DM-1701 dmrconf binary read succeeded. Offline decode passed and SHA-256 was verified in the private manifest |
| Bootable stock recovery image | PASS | OPEN | Radioddity V02.03 CSV written and operator verified normal boot and operation, menu `V002.003`. Original `D012.006` was not dumped |
| Factory calibration preservation | OPEN for next write | OPEN | No factory calibration dump. The tested V02.03 write excluded external SPI. Verify that the next plan also leaves calibration untouched |
| Bootloader/update route identified | PASS | OPEN | Factory USB DFU and `radio_tool` 0.5.1 application-only write tested on DM-1701 |
| Stock FM/DMR smoke tests documented | PASS (pre-update) | PASS | Operator reported analog FM and DMR TX/RX before the update. After V02.03, operator confirmed general operation but no separate mode-by-mode or instrumented results were recorded |
| RF load/attenuation and SDR input power verified | OPEN | OPEN | |
| Human approved specific flash / TX operation | OPEN | OPEN | |

*An OPEN gate means no device-write or RF-TX operation is permitted.*

## DM-1701 host evidence | 2026-11-24

LAB-004, M17-001 and the local LAB-009 build passed on the computer. UHD is installed. LAB-003 device inventory, LAB-006 fixture verification, LAB-007 instrumented stock captures, factory calibration readback and LAB-008 on-radio validation remain open. The [exact offline erase/write preview and bench worksheet](dm1701-bench.md) cover the plain comparison build. The tested stock fallback is still installed. NOT RUN ON HARDWARE.

The [M17 frame-generator test build](dm1701-m17-frame-build.md) has its own private DMR-codec-merged image, reproducible checksum and nine-sector offline write preview. Its read-only diagnostic passed in CPU emulation. Hardware gates remain open.

## LibreSDR receive path | 2026-11-25

LAB-003 passed for the connected LibreSDR on USB 3 with the qualified FPGA image: channel 0 sustained 960 ksample/s for five seconds with zero drops, overruns and RX timeouts. [Image selection, exact hashes, commands and results](../hardware/libresdr/qualification.md). LAB-006 fixture verification and LAB-007 instrumented stock-radio captures remain open. The DM-1701 firmware and RF gates are unchanged.

The [physical PTT test image and its sector-by-sector preview](dm1701-m17-ptt.md) passed the host radio-core and independent GNU Radio decoder tests. The DM-1701 to LibreSDR RF result is pending. The stock firmware is still installed.
