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
