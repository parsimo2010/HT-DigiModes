# Ham Digital Modes Lab

A research lab to develop standalone M17 on a Baofeng DM-1701 and host-assisted RADE BBFM on a verified compatible handheld, using a LibreSDR reference station. The second radio is confirmed as a DM-1801 Pro, but its board revision and cable still need verification.

**Live-air testing is underway.** On 425.525 MHz the DM-1701 sent six M17 data frames to the LibreSDR. GNU Radio decoded all 96 expected bytes. The handheld runs the personalized RadioFoundry PTT build. Radioddity V02.03 CSV is its tested stock fallback. [Bench report and measurements](notes/dm1701-m17-first-rf.md).

**Next session on native Linux.** Bring the private transfer archive, replay the known recording, then work toward receiving an SDR-generated burst on the handheld. The handoff includes the package list, qualified SDR images, commands and expected payload hash. [Next-session handoff](notes/next-session.md) · [Development plan](docs/DEVELOPMENT_PLAN.md) · [Lab instructions](AGENTS.md).

## Host-only quick start

From the checkout root, run with Python 3.8+ (use `python` on Windows).

```bash
python3 scripts/lab.py status
python3 -m unittest discover -s tests -v
```

The [GNU Radio reference vectors](notes/m17-reference.md), [RadioFoundry build](notes/dm1701-build.md) and [LibreSDR qualification](hardware/libresdr/qualification.md) document the pieces used for the live test. Firmware, factory backups, station identifiers and RF recordings stay in private storage.

**Upstream references:** <https://github.com/RadioFoundry/RadioFoundry>, <https://github.com/M17-Project/gr-m17>, <https://github.com/drowe67/radae>.
