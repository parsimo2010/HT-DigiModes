# Safety/recovery gates

The operator has confirmed basic FM/DMR operation and separately approved the DM-1701 codeplug read. No restore, device write, or RF engineering operation is approved by this record. For every hardware operation, record:

| Gate | DM-1701 | DM-1801 | Evidence / date / approval |
|---|---|---|---|
| Exact model and interface verified | OPEN | OPEN | |
| Stock codeplug saved and hash recorded | PASS | OPEN | DM-1701 dmrconf binary read succeeded. Offline decode passed and SHA-256 was verified in the private manifest |
| Factory firmware/codec/calibration backup or verified recovery plan | OPEN | OPEN | |
| Bootloader/update route identified | OPEN | OPEN | |
| Stock FM/DMR smoke tests documented | PASS | PASS | Operator reported analog FM and DMR TX/RX on 2026-11-24. No instrumented measurements |
| RF load/attenuation and SDR input power verified | OPEN | OPEN | |
| Human approved specific flash / TX operation | OPEN | OPEN | |

*An OPEN gate means no device-write or RF-TX operation is permitted.*
