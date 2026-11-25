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

RadioFoundry's generic stock-backup instructions only apply to selected radios. Its [pinned DM-1701 board configuration](https://github.com/RadioFoundry/RadioFoundry/blob/bac4b209cd8ade5de3040ed7df11753b9e0ceacc/boards/dm1701/board.toml) declares stock backup unavailable. A backup taken after installing new firmware cannot recover the original application it replaced. A stock codeplug export and a vendor recovery package are useful separately, but neither proves a full copy of the installed firmware or unit-specific calibration.

- **Installed firmware:** RadioFoundry reports STM32 RDP Level 1 on a reference DM-1701. This unit's protection state was not probed. Dropping Level 1 to Level 0 mass-erases internal flash, so unlocking is not a backup method. See the [DM-1701 hardware notes](https://radiofoundry.org/docs/spec/hardware-dm1701) and [STM32F4 reference manual](https://www.st.com/resource/en/reference_manual/rm0090-stm32f4xx-reference-manual-stmicroelectronics.pdf).
- **Recovery package:** Both archived DM-1701 V02.06 variants (CSV and noCSV) were staged outside Git and matched the [published reference hashes](https://radiofoundry.org/docs/spec/codec-dm1701). A host-only inspection did not establish that either one matches menu firmware `D012.006`. Confirm the exact board and firmware variant with Baofeng/Radioddity before choosing an image.
- **Calibration:** Factory values are in separate SPI flash security registers and are absent from the codeplug export. RadioFoundry [documents preserving them during its first install](https://radiofoundry.org/docs/dev/web-flasher) and reading them after the install. Verify the exact first-install plan is confined to MCU application flash, and defer any stock-codeplug migration or other SPI operation until calibration has been read and archived. No calibration preservation has been measured on this unit. A pre-flash board-level read is a separate bench option if the exact proposed flash path cannot prove it leaves calibration alone.

### Application readback and evidence

The normal stock application and the factory bootloader have the same USB VID:PID. The [bootloader descriptor](https://radiofoundry.org/docs/spec/hardware-dm1701#151-entering-the-bootloader) places MCU application flash at `0x0800C000`. That descriptor identifies the mode, not whether the device honors reads.

[ClearDMR](https://cleardmr.com/) advertises stock application backup in bootloader mode and its page script attempts standard DfuSe upload. Its fixed backup ceiling is 819,200 bytes, whereas the two archived V02.06 containers have 889,856 and 901,120 bytes of internal application segments. A produced file alone is therefore not proof of completeness. [RadioFoundry's account](https://radiofoundry.org/docs/dev/web-flasher) says the stock bootloader cannot read program flash. [radio_tool](https://github.com/v0l/radio_tool) reports bootloader dumping and application writing on a DM-1701, not installed application dumping. The 48 KiB bootloader mirror is not the application.

To distinguish those claims on this unit, first identify factory bootloader mode from its descriptor, then, with operator approval, try a bounded upload of the first 2 KiB of the application using dfu-util. Accept no short, all-zero, erased, or implausible vector-table result as firmware. The first-block fingerprints of the CSV and noCSV vendor candidates differ. A plausible or matching first block is evidence to justify a separate, bounded full-application read, not proof of a full backup or an exact firmware match. For a full backup, require correct range and length, independent repeated reads with matching hashes, and spot checks against known application data. Do not use erase, unprotect, force, or write options. The probe has not been run on this unit.

The recovery gate stays open. Host-only work can proceed, starting with the GNU Radio M17 reference loopback and a reproducible DM-1701 build that is not flashed.
