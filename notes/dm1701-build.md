# LAB-009 | DM-1701 host build, 2026-11-24

Two forced builds of pinned RadioFoundry produced the same 707,004-byte plain application. SHA-256 is `a1930d2b91248f04952553997fe9d5511860f5d237dec383c96fd7df77f017cd`. The binary is at `~/ht-m17/RadioFoundry/build/dm1701/rfoundry_dm1701.bin` in Ubuntu WSL, outside the lab checkout. Linker use was 707,004 / 737,280 bytes of application flash, 127,384 / 131,068 bytes of main RAM and 65,280 / 65,536 bytes of CCM RAM. That leaves only 256 bytes of CCM headroom in the baseline layout.

The codec directory contained no proprietary image. The local build has no stock AMBE codec merged and no M17 code linked. The separate M17 host tests exercise the lab framer. This baseline is for build comparison. A first installation intended to preserve DMR voice needs its own private codec-merged image, checksum and new erase/write preview.

`make -j8 -C tests/host` exited 0. The final run included tshark packet validation, the DM-1701 family calibration tests and 2,678 UI flows in the color configuration. Upstream skipped its private Tier III recording replay and standard SNMP MIB check (MIB definitions absent). Logs are outside Git in `~/ht-m17/rf-tests-final.log` and `rf-fixed2.log`.

## Repeat on a fresh Ubuntu 26.04 x86_64 host

Install git, build-essential, gcc-arm-none-eabi, libnewlib-arm-none-eabi, python3, python3-pytest, python3-serial, python3-numpy, tshark and snmp from apt. Tested GNU Make 4.4.1, GCC 15.2.0 (host), arm-none-eabi-gcc 14.2.1 20241119 (package 15:14.2.rel1-1), binutils-arm-none-eabi 2.45.50.20251209-1ubuntu1+23build1 and libnewlib-arm-none-eabi 4.6.0.20260123-1. Use the upstream origin URL and a clean source tree so the embedded revision metadata matches.

```bash
set -eu
mkdir -p ~/ht-m17
cd ~/ht-m17
git clone https://github.com/RadioFoundry/RadioFoundry
cd RadioFoundry
git checkout --detach bac4b209cd8ade5de3040ed7df11753b9e0ceacc
git submodule update --init --jobs 5
git submodule status
make -j8 -C tests/host
export SOURCE_DATE_EPOCH=$(git show -s --format=%ct HEAD)
make -B -j8 BOARD=dm1701 'OPT=-Os -frandom-seed=dm1701'
sha256sum build/dm1701/rfoundry_dm1701.bin
```

The initial default build had hash `8a238adef3f76d1db288168aeab835c544428fa80e4fa7776ca88d28cef72ccc`; a forced rebuild differed. The pinned source uses C build date/time in the CPS interface. The recorded recipe fixes the epoch to 1795558828 and the compiler random seed. Repeating the last two commands reproduced the checksum above. A different build directory or toolchain was not qualified for that checksum.

NOT RUN ON HARDWARE. [Offline memory preview and bench gates](dm1701-bench.md).
