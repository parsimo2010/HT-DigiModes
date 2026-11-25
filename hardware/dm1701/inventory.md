# DM-1701 inventory

| Field | Status |
| --- | --- |
| Literal model label and board revision | Pending operator verification |
| Firmware version before update | `D012.006` (operator-reported, not dumped) |
| CP version before update | `V01.05` (operator-reported) |
| Firmware written | Radioddity V02.03 CSV. Updater completed, normal boot and menu version pending operator verification |
| Expected cable/interface | Model-specific native USB cable, no USB-to-UART converter |
| Host USB observation | See the [arrival log](../../notes/arrival-session.md) |
| Analog FM and DMR baseline | Operator confirmed transmit and receive in both modes before the update. V02.03 not yet checked |
| Stock codeplug | Binary backup saved privately, decoded offline, and SHA-256 verified |
| Firmware and factory calibration backup | Not captured. The expected working calibration window in the codeplug dump was all zero |
| Stock recovery package | Both Radioddity V02.03 variants and two V02.06 candidates were staged privately and their hashes checked. V02.03 CSV was written. A bootable recovery image is not yet verified |

Keep serial numbers, radio IDs, label photos, and full USB instance paths in private storage outside the checkout.
