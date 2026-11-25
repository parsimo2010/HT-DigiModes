# LibreSDR USB and FPGA trials, 2026-11-25

Ubuntu 26.04 under WSL2, UHD 4.9.0.1-1ubuntu1. The operator believes the unit has an XC7A200T. Treat this as an operator identification pending a board marking. Windows host inventory saw one WestBridge 2500:0020. After volatile FX3 firmware loading, that SDR re-enumerated from USB bus 3-1 to 3-2. Reattaching it to Ubuntu allowed UHD discovery as product B210, type b200. The separate handheld was left on Windows.

## Image inventory

| User-supplied file | SHA-256 of FPGA bytes | Offline evidence |
|---|---|---|
| XC7A200T archive, member usrp_b210_fpga.bin | `11d2e61fb978fcce90cf012daaca671b3fbc5918aa6ea00de3e848888e479299` | Archive README specifies xc7a200tfbg484-1, Vivado 2024.1. IDCODE word 03636093 |
| libresdr_b210.bin and usrp_b210_fpga (2).bin | `7322a2a9052520c8a50646e773bd7359e683cc9bdcf159ee9068753751246ce5` | Identical bytes and same IDCODE. Matches the [B220 Mini repository binary](https://github.com/NustyFrozen/LibreSDR-UHD-B220-Mini/blob/dadb9226d9db4e9ef284595a03c0e0d0890b79dc/linux/libresdr_b210.bin) |
| Loose usrp_b210_fpga.bin | `c503101c6c130fe43f253b969d2a09f28b7cd7392389e73a3598a5305df89005` | Same IDCODE. Matches the [B220 Mini project binary](https://github.com/bkerler/LibreSDR_UHD_B220_Mini_FPGA/blob/9e5c301e6677b429a8217c9c0c3d12abd91826ff/usrp_b210_fpga.bin) |
| XC7A75T archive, member usrp_b210_fpga.bin | `c8b39f9cc08572091492fba21bac3c636be2dc7639cf8d157f0c4cc6e9450c90` | Different target IDCODE 03632093. Excluded from 200T trial |
| Loose usrp_b210_fpga (1).bin | `0ab54295961c881cfe37398ce96514063a1cc7fac8035b7ae5ff63844d03bdca` | Different target IDCODE 03631093. Excluded from 200T trial |

SHA-256 of the original 200T ZIP is `a96eafa40c86ca2d191ee02d32cc9c57bdb5347a0f8946949807370566daa9b1`. The IDCODE values are in the files themselves. A matching FPGA part can still have different board wiring. The vendor publishes separate Artix-7 board images. [Vendor repository](https://github.com/OpenSourceSDRLab/USRP-B210-Artix-7-AD9361)

## Device observations

Host preparation used an isolated `~/ht-m17/libresdr/trial-200t` directory and `uhd_images_downloader -t '^b2xx_common_fw_default$' -i "$PWD" -T` from that directory. The B2xx FX3 runtime file `usrp_b200_fw.hex` has SHA-256 `cc8e4bc968d91d1a67c63871ce5b2c1613c49676fe363bf2f6e336059899ae5c`. The `.img` bootloader file in the package was unused.

Windows commands used were usbipd list, bind and attach for the SDR. With `UHD_IMAGES_DIR=$PWD`, the first `timeout 30 uhd_find_devices --args type=b200` loaded FX3 RAM. Discovery succeeded after USB re-enumeration and reattachment. `timeout 60 uhd_usrp_probe --args "type=b200,fw=$PWD/usrp_b200_fw.hex,fpga=$PWD/usrp_b210_fpga.bin"` selected the 200T ZIP member. UHD reported USB 3 and then a register acknowledgement timeout (`wait_for_ack`, `accum_timeout < _timeout`). Reopening with the same arguments failed again. The ZIP image did not qualify on this setup. USB discovery by itself does not establish FPGA or receive streaming compatibility.

Qualification requires a successful initialized probe and nonzero RX samples in a five-second 960 ksample/s test with no drops, overruns, sequence errors or timeouts. The [M17 receiver and replay results](../../docs/libresdr-inventory.md) are tested independently of the SDR. Raw USB/UHD logs stay outside Git.
