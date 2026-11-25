# Safety/recovery gates

The operator confirmed basic FM/DMR operation before any change and separately approved the DM-1701 codeplug read and the one Radioddity V02.03 CSV application write recorded in the arrival log. Those approvals do not carry over to a future write or RF operation. For every hardware operation, record:

| Gate | DM-1701 | DM-1801 | Evidence / date / approval |
|---|---|---|---|
| Exact model and interface verified | OPEN | OPEN | |
| Stock codeplug saved and hash recorded | PASS | OPEN | DM-1701 dmrconf binary read succeeded. Offline decode passed and SHA-256 was verified in the private manifest |
| Factory firmware/codec/calibration backup or verified recovery plan | OPEN | OPEN | |
| Bootloader/update route identified | OPEN | OPEN | |
| Stock FM/DMR smoke tests documented | PASS (pre-update) | PASS | Operator reported analog FM and DMR TX/RX on 2026-11-24. No instrumented measurements. DM-1701 V02.03 test pending |
| RF load/attenuation and SDR input power verified | OPEN | OPEN | |
| Human approved specific flash / TX operation | OPEN | OPEN | |

*An OPEN gate means no device-write or RF-TX operation is permitted.*
