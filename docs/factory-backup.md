# Factory backup checklist

1. Record the literal model, hardware revision if shown, and installed firmware version and variant from the radio. Keep photos, serials and DMR IDs outside the checkout. Do not select any DM-1801 tooling until its variant is confirmed.
2. For a stock DM-1701 on Windows, start with the model-specific [Baofeng CPS download](https://www.baofengradio.com/pages/download) and [Radioddity programming guide](https://dm-1701.s3.amazonaws.com/Baofeng%20DM-1701%20Programming%20Guide%20V1.0_Radioddity_.pdf). Use the USB driver documented for the chosen tool. Do not swap drivers just to make a generic DFU utility see the device.
3. After confirming the exact device, tool version and operation, use the supported **read-from-radio** codeplug workflow. Save the original unchanged outside the checkout. Reopen the saved file locally to verify it parses. Do not upload anything as a backup check.
4. Separately identify the exact recovery image and a supported way to preserve the original firmware, calibration and codec. Review the tool's report and record what it actually saved and what it couldn't read. A codeplug export, vendor update package and full device backup are not interchangeable.
5. Keep a second copy offline. Record UTC time, tool version, source URL, file size and SHA-256 for each artifact in a private manifest. Compare both copies' hashes.

Hash only the local files you saved. These commands do not access the radio.

```bash
sha256sum -- "/path/outside/the/repo/original.rdt"
```

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath 'C:\path\outside\repo\original.rdt'
```

Keep the [recovery gates](../notes/gates.md) open until the corresponding evidence exists. Record only sanitized status in the public repo.

## Stock DM-1701 limitation

RadioFoundry's generic stock-backup instructions only apply to selected radios. Its [pinned DM-1701 board configuration](https://github.com/RadioFoundry/RadioFoundry/blob/bac4b209cd8ade5de3040ed7df11753b9e0ceacc/boards/dm1701/board.toml) declares stock backup unavailable. Do not install replacement firmware to gain access to a backup tool. For now, plan for a standalone factory codeplug export and a separate, version-matched vendor recovery package. Neither proves a full copy of the installed firmware or unit-specific calibration.
