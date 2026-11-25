"""Run the pinned test build's M17 debug view in a Thumb CPU emulator.

Use the final DM-1701 binary and its own unstripped ELF. No device is opened.
"""
import argparse
import json
from pathlib import Path
import struct
import subprocess

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_MODE_MCLASS
from unicorn.arm_const import (
    UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,
    UC_ARM_REG_SP,
)


def render_view(image, elf):
    symbols = subprocess.check_output(["arm-none-eabi-nm", "--defined-only", elf], text=True)
    # GCC can split the range check from the switch when link-time optimization is on.
    entries = {s[2]: int(s[0], 16) for line in symbols.splitlines() if len(s := line.split()) == 3}
    entry = entries.get("debuglink_view_section") or entries["debuglink_view_section.part.0"]
    cpu = Uc(UC_ARCH_ARM, UC_MODE_THUMB | UC_MODE_MCLASS)
    flash, ram = 0x0800c000, 0x20000000
    cpu.mem_map(flash, 0xf4000)
    cpu.mem_write(flash, image.read_bytes())
    cpu.mem_map(ram, 0x20000)
    # ARM dl_text_t {char *buf, size_t cap, size_t len, bool full}.
    buffer = ram + 256
    cpu.mem_write(ram, struct.pack("<IIIBxxx", buffer, 512, 0, 0))
    stop = ram + 0x1000
    cpu.reg_write(UC_ARM_REG_R0, 39)  # appended M17 section at this revision
    cpu.reg_write(UC_ARM_REG_R1, 0)   # the M17 renderer needs no radio state
    cpu.reg_write(UC_ARM_REG_R2, ram)
    cpu.reg_write(UC_ARM_REG_SP, ram + 0x20000)
    cpu.reg_write(UC_ARM_REG_LR, stop | 1)
    cpu.emu_start(entry | 1, stop, count=1_000_000)
    length, full = struct.unpack("<IB", cpu.mem_read(ram + 8, 5))
    if cpu.reg_read(UC_ARM_REG_PC) != stop or full or length > 512:
        raise ValueError("M17 view failed to return a complete reply")
    return bytes(cpu.mem_read(buffer, length)).decode("ascii")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path)
    parser.add_argument("elf", type=Path)
    args = parser.parse_args()
    text = render_view(args.image, args.elf)
    fields = dict(line.split("=", 1) for line in text.splitlines())
    if fields["section"] != "m17":
        raise ValueError("Unexpected debug view")
    vector_path = Path(__file__).resolve().parents[1] / "tests/vectors/m17-loopback.json"
    vectors = json.loads(vector_path.read_text())
    levels = (1, 3, -1, -3)
    for key, name in (("m17.lsf", "link_setup"), ("m17.stream0", "stream_0000")):
        data = bytes.fromhex(fields[key])
        bits = "".join(f"{b:08b}" for b in data)
        symbols = [levels[(b >> shift) & 3] for b in data for shift in (6, 4, 2, 0)]
        if bits != vectors[name]["bits"] or symbols != vectors[name]["symbols"]:
            raise ValueError(f"{key} differs from GNU Radio capture")
    print(text, end="")


if __name__ == "__main__":
    main()
