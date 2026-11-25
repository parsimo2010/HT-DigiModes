# DM-1701 M17 frame-generator test build

**Built and tested on the computer. NOT RUN ON HARDWARE.** The optional `m17` debug view computes a link setup frame and stream frame 0000 from fixed inputs when read. Each result is a 48-byte, MSB-first packed dibit record. It uses RadioFoundry's convolutional and extended Golay encoders. The M17 diagnostic has no PTT, modem, settings or storage calls. The rest of the image is RadioFoundry firmware with its normal radio functions. The local merge includes the operator's stock AMBE+2 for DMR. M17 voice (Codec2), an M17 channel/menu and bounded M17 modem output are still outstanding.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| Plain test application | 707,856 | `d38666db5e53f6b3d0f43d0c5b59450fc2ee7e119d2364c0bb6e6d08db0539ea` |
| Private test image with DMR codec | 999,424 | `ba046925b5fe997dc0f1e98535a62dfe6f4d3b33b55a58217fb1e5666565395f` |

The private copy is under `HT-DigiModes-Private/test-builds/c116f874/` in the operator's Windows home directory. A forced rebuild and second offline merge matched it byte for byte. The linker used 127,384 bytes of main RAM and 65,280 bytes of CCM RAM. Static RAM use matches the previous baseline. This does not measure task stack use on the handheld.

## Verification

- The upstream host suite, including the new `m17FrameTest`, exited 0. Its private Tier III recording replay and standard SNMP MIB check were skipped. All eight lab tests passed. The firmware built with the feature enabled and disabled. The enabled build emitted zero compiler warnings.
- Unicorn 2.1.4 executed the M17 debug-view branch **from the merged image bytes**, using the symbol address from its companion ELF and emulated RAM. Both results matched all 384 bits and 192 symbols of their [GNU Radio reference records](../tests/vectors/m17-loopback.json). This exercises the compiled section renderer. USB traffic, radio boot and the RF path have no measured result.
- In the pinned gr-m17 environment, a GNU Radio vector source supplied the two emulated frame outputs between the reference preamble and end marker. The independent decoder reported AB1CDE to AB2CDE, type 0003, frame 0000, payload `00000000000000000001020304050600`, metric `e=0.0`.
- `python3 tools/check_doc_links.py` reported zero broken links and `python3 tools/bringup.py check` reported zero errors. The [source patch](../firmware/radiofoundry/m17-frame-test.patch) applies cleanly to the pinned RadioFoundry revision.

## Offline preview of this specific merged image

The pinned writer's model-checked dry run would erase **and program** all nine MCU application sectors. End addresses are exclusive. It would program 976 contiguous 1 KiB blocks from 0x0800C000 to 0x08100000, including application, fill bytes, relocated DMR codec and descriptor.

| Sector | Start | End | Blocks |
|---|---|---|---:|
| 3 | 0x0800C000 | 0x08010000 | 16 |
| 4 | 0x08010000 | 0x08020000 | 64 |
| 5 | 0x08020000 | 0x08040000 | 128 |
| 6 | 0x08040000 | 0x08060000 | 128 |
| 7 | 0x08060000 | 0x08080000 | 128 |
| 8 | 0x08080000 | 0x080A0000 | 128 |
| 9 | 0x080A0000 | 0x080C0000 | 128 |
| 10 | 0x080C0000 | 0x080E0000 | 128 |
| 11 | 0x080E0000 | 0x08100000 | 128 |

The plan excludes bootloader sectors 0–2 and all external SPI storage, including the factory calibration registers. The final zero-length request at 0x08000000 is the writer's reset step. The preview covers updater operations only. Physical SDR inventory, fixture verification, stock RF measurements and per-operation approval are open. After any separately approved first boot, verify and save the factory calibration privately before settings changes or RF. See [bench gates](dm1701-bench.md).

## Repeat the computer-only checks

Use the Ubuntu 26.04 Arm toolchain and packages in [LAB-009](dm1701-build.md), plus `python3-unicorn`. From the lab root, with the pinned RadioFoundry checkout and its submodules in `~/ht-m17/RadioFoundry`, use a fresh worktree. The local commit identity and committer date below reproduce the revision embedded in the image. Supply `STOCK_CSV` as the private path to the verified V02.03 CSV file.

```bash
set -eu
lab=$PWD
cd ~/ht-m17/RadioFoundry
export RFOUNDRY_THIRD_PARTY="$PWD/third_party"
tools/worktree.sh add ../rf-m17-rebuild --detach bac4b209cd8ade5de3040ed7df11753b9e0ceacc
cd ../rf-m17-rebuild
git -c user.name='HT DigiModes Lab' -c user.email='lab@localhost' am --committer-date-is-author-date "$lab/firmware/radiofoundry/m17-frame-test.patch"
test "$(git rev-parse HEAD)" = c116f87424eba7735dc112b820a24e96e7e2203b
make -j8 -C tests/host
export SOURCE_DATE_EPOCH=$(git show -s --format=%ct HEAD)
make -j8 BOARD=dm1701 CONFIG_M17_FRAME_TEST=y 'OPT=-Os -frandom-seed=dm1701'
img=build/dm1701/rfoundry_dm1701
umask 077
python3 tools/codec_extract.py --board dm1701 --stock "${STOCK_CSV:?Set private V02.03 CSV path}" --image "$img.bin" -o "${img}_codec.bin"
sha256sum "$img.bin" "${img}_codec.bin"
python3 "$lab/scripts/check_m17_image.py" "${img}_codec.bin" "$img.elf"
python3 tools/stm32_dfu.py --model dm1701 --dry-run "${img}_codec.bin"
cd "$lab"
python3 -m unittest discover -s tests -v
```

The upstream checkout retains its LICENSE, AUTHORS and attribution. The lab tracks only the source patch, emulator check and evidence. Firmware, stock files and codec bytes stay outside the lab repository.
