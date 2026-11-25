# First DM-1701 M17 transmission received by LibreSDR

**Hardware result, 2026-11-25.** On 425.525 MHz simplex, the operator keyed the DM-1701 and the LibreSDR received a complete M17 data burst. GNU Radio decoded the operator’s station address, the broadcast destination, TYPE 0003, and frames 0000, 0001, 0002, 0003, 0004 and 8005. The last number has the end-of-stream bit set. Each frame contained the exact 16-byte ramp from 00 through 0f. The 96 decoded bytes had SHA-256 `6c6b011011c3e8b3086372c9e52bdc83294796bf7b9150ab099e9314052c106f`.

## Install and backup

The factory USB bootloader identified its internal application base at 0x0800C000. The pinned writer installed the [original vector build](dm1701-m17-ptt.md), and the running handheld reported DM-1701 revision 4c6a56e5. Its two M17 debug frames matched the reference data directly over USB.

Before changing the VFO or transmitting, CPS read area 10 at 0x1000, 0x2000 and 0x3000 twice, 256 bytes per read. Both readbacks matched. The two calibration banks passed the board's power and gain row checks after in-memory conversion. The private backup ZIP and its hashes were verified, then a second identical copy was verified in WSL. Both copies reside on the same computer. The tested stock recovery remains Radioddity V02.03 CSV.

The radiated test used a private variant with the operator's source address and broadcast destination. The lab encoder first reproduced the original vector exactly. Re-encoding the address and dependent check bits changed 147 bytes inside the 432-byte static vector at 0x080B0000. The plain application code and merged codec bytes matched the first build. The personalized merged image's SHA-256 is `60fd549d08b955232a62f0dd243f6792f1e61d7f8439dbbe207926b52fb9d4ee`. Both installations used the pinned stock DFU writer, with a model-checked dry run followed by `python3 tools/stm32_dfu.py --model dm1701 --key "$key" "$image"`. Each programmed 976 contiguous 1 KiB blocks over sectors 3–11, from 0x0800C000 up to 0x08100000 exclusive. Bootloader sectors 0–2 and external calibration were outside both plans. After the second boot, the entire transmit vector read from MCU flash matched the personalized file, and all three security registers matched the backup again.

## RF measurements

Both endpoints used separate stub antennas a few feet apart. The LibreSDR had stubs on all four connectors. The host used channel A RX2, 0 dB requested RX gain, 960 ksample/s, complex float32. The handheld used physical SK1 followed by PTT and the bench firmware's power level zero.

| Measurement | Second key-down |
|---|---:|
| RF present, 1 ms bins | 420 ms |
| Nominal vector duration | 360 ms |
| Frame spacing measured across LSF and six stream frames | 40.00 ms |
| Fitted symbol rate, relative to SDR clock | 4,800 symbols/s |
| Carrier offset relative to SDR tuning | −765 Hz |
| Estimated outer deviation (four-level FSK) | ±2.40 kHz |
| Estimated 99% occupied bandwidth | 9.67 kHz |
| Median level during burst / idle in the 960 kHz capture | −41.7 / −78.3 dBFS |
| Largest absolute I or Q component | 0.0194 full scale |

The 420 ms interval includes modem key-up and tail. Frame correlations used the known symbols and nominal chip pulse shape. The fit estimates frequency offset and deviation from the demodulated signal. Bandwidth used a two-sided Welch spectrum over the burst interior with the noise floor subtracted. These are single-capture estimates against the SDR clock. Absolute transmit power, standards compliance, M17 voice and handheld M17 receive were outside this test.

The first, short press produced about 235 ms of RF. With frequency correction the decoder recovered three correct payloads and an incomplete transmission that failed the full check. On the second, longer press the receiver at its nominal center recovered zero frames. Replaying the same unmodified samples with a −750 Hz carrier offset recovered all six payloads. The radio reported two physical PTT downs, a final TX elapsed display value of 460 ms, keys released, and idle on 425.525 MHz. The firmware ended the second burst while the operator held PTT.

## Reproduce from the saved samples

The private session folder is `HT-DigiModes-Private/dm1701-install-4c6a56e5-7unTnY` in the Windows home directory. It contains the factory backup, both writer logs and previews, personalized image and vector, the raw burst window, decoder log, payload, metrics and plot. The original longer captures remain in the WSL private session directory. The cropped raw IQ file has SHA-256 `9fe1d1a60f57ea2085af00492b14dc56111996a7650f5956567f01b76bbad0c0`.

From the lab root in Ubuntu, set `SESSION` to that private session directory. The same receive graph was used for the independent decoder and the offline replay.

```bash
source ~/ht-m17/env.sh
python3 scripts/m17_rx.py --iq "$SESSION/m17-rf-burst.cf32" --rate 960000 --seconds 2 \
  --carrier-offset-hz=-750 --check-ramp --expect-frames 6
python3 scripts/m17_burst_metrics.py "$SESSION/m17-rf-burst.cf32" "$SESSION/station-vector.bin"
```

The lab host suite passed eight tests and RadioFoundry's radio-core M17 host test passed 45 checks. A synthetic 4,800-symbol/s burst with +430 Hz carrier error and ±2,400 Hz outer deviation also verified the measurement estimator.
