# Safety/recovery gates

The operator confirmed basic FM/DMR operation before any change and separately approved the DM-1701 codeplug read and the one Radioddity V02.03 CSV application write recorded in the arrival log. Those approvals do not carry over to a future write or RF operation. For every hardware operation, record:

| Gate | DM-1701 | DM-1801 | Evidence / date / approval |
|---|---|---|---|
| Exact model and interface verified | USB/DFU VERIFIED | PRO IDENTIFIED | DM-1701 native USB and factory update mode were used successfully. Board revisions and DM-1801 Pro cable remain unverified |
| Stock codeplug saved and hash recorded | PASS | OPEN | DM-1701 dmrconf binary read succeeded. Offline decode passed and SHA-256 was verified in the private manifest |
| Bootable stock recovery image | PASS | OPEN | Radioddity V02.03 CSV written and operator verified normal boot and operation, menu `V002.003`. Original `D012.006` was not dumped |
| Factory calibration preservation | PASS | OPEN | Three complete factory security registers saved privately after first boot and verified again after the station-specific update |
| Bootloader/update route identified | PASS | OPEN | Factory USB DFU and `radio_tool` 0.5.1 application-only write tested on DM-1701 |
| Stock FM/DMR smoke tests documented | PASS (pre-update) | PASS | Operator reported analog FM and DMR TX/RX before the update. After V02.03, operator confirmed general operation but no separate mode-by-mode or instrumented results were recorded |
| Conducted RF fixture | OPEN | OPEN | First M17 measurement used separate stub antennas in the operator-selected radiated setup |
| Specific flash / TX operation | COMPLETED | OPEN | Operator authorized the DM-1701 install and performed both physical PTT tests on 425.525 MHz |

Apply open gates to their corresponding operations. The operator may explicitly defer the stock RF baseline and choose a radiated test. Record application installation, factory readback and RF evidence separately.

## DM-1701 host evidence | 2026-11-24

LAB-004, M17-001 and the local LAB-009 build passed on the computer. UHD is installed. LAB-003 device inventory, LAB-006 fixture verification, LAB-007 instrumented stock captures, factory calibration readback and LAB-008 on-radio validation remain open. The [exact offline erase/write preview and bench worksheet](dm1701-bench.md) cover the plain comparison build. The tested stock fallback is still installed. NOT RUN ON HARDWARE.

The [M17 frame-generator test build](dm1701-m17-frame-build.md) has its own private DMR-codec-merged image, reproducible checksum and nine-sector offline write preview. Its read-only diagnostic passed in CPU emulation. Hardware gates remain open.

## LibreSDR receive path | 2026-11-25

LAB-003 passed for the connected LibreSDR on USB 3 with the qualified FPGA image: channel 0 sustained 960 ksample/s for five seconds with zero drops, overruns and RX timeouts. [Image selection, exact hashes, commands and results](../hardware/libresdr/qualification.md). LAB-006 fixture verification and LAB-007 instrumented stock-radio captures remain open. The DM-1701 firmware and RF gates are unchanged.

The [physical PTT test image and its sector-by-sector preview](dm1701-m17-ptt.md) passed the host radio-core and independent GNU Radio decoder tests. The DM-1701 to LibreSDR RF result is pending. The stock firmware is still installed.

## Proposed 425.525 MHz simplex test

The operator reports that the DM-1701 is in DFU and that the DM-1701 and LibreSDR each have a stub antenna a few feet apart in open air. There is no coupler or attenuator. LAB-006 remains open. The separation and burst duration do not establish a maximum peak input level for the SDR. The instrumented stock baseline is also outstanding.

The private candidate’s SHA-256 matched the build record. The pinned writer completed an offline DM-1701 dry run using the model key verified from the private stock package. The plan covers 976 blocks in MCU sectors 3–11, from 0x0800C000 up to 0x08100000 exclusive. The bootloader and external calibration registers are outside the write plan. No USB, flash or RF operation was performed. The factory calibration backup is pending first boot.

## Completed DM-1701 radiated test

The operator deferred the instrumented stock baseline. The handheld booted the M17 test firmware, the factory calibration was saved privately, and the SDR independently decoded six correct data frames over RF. The prior open-air proposal and host-only notes above are historical. [Install, measurements and capture replay](dm1701-m17-first-rf.md).
