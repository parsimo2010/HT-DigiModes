# DM-1701 inventory

| Field | Status |
| --- | --- |
| Literal model label and board revision | Pending operator verification |
| Firmware version shown in menu | `D012.006` (operator-reported, not yet mapped to a vendor recovery image) |
| CP version shown in menu | `V01.05` (operator-reported) |
| Expected cable/interface | Model-specific native USB cable, no USB-to-UART converter |
| Host USB observation | See the [arrival log](../../notes/arrival-session.md) |
| Analog FM and DMR baseline | Operator confirmed transmit and receive in both modes |
| Stock codeplug | Binary backup saved privately, decoded offline, and SHA-256 verified |
| Firmware and factory calibration backup | Not captured. The expected working calibration window in the codeplug dump was all zero |

Keep serial numbers, radio IDs, label photos, and full USB instance paths in private storage outside the checkout.
