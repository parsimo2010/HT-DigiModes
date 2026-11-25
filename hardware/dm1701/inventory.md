# DM-1701 inventory

| Field | Status |
| --- | --- |
| Literal model label and board revision | Pending operator verification |
| Firmware version before update | `D012.006` (operator-reported, not dumped) |
| CP version before update | `V01.05` (operator-reported) |
| Current firmware | Radioddity V02.03 CSV. Operator confirmed normal boot and operation, menu `V002.003` |
| Expected cable/interface | Model-specific native USB cable, no USB-to-UART converter |
| Host USB observation | See the [arrival log](../../notes/arrival-session.md) |
| Analog FM and DMR baseline | Operator confirmed transmit and receive in both modes before the update. V02.03 operation reported generally, with no separate mode-by-mode or instrumented results |
| Stock codeplug | Binary backup saved privately, decoded offline, and SHA-256 verified. Operator does not require carrying the stock channels into M17 |
| Original firmware and factory calibration backup | Not captured. The expected working calibration window in the codeplug dump was all zero. The V02.03 write plan excluded external flash |
| Stock recovery package | Radioddity V02.03 CSV tested on this radio. Other staged variants are not verified fallbacks for this unit |

Keep serial numbers, radio IDs, label photos, and full USB instance paths in private storage outside the checkout.
