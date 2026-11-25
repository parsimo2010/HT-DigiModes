# Ham Digital Modes Lab — Codex starter

A research lab to develop standalone M17 on a Baofeng DM-1701 and host-assisted RADE BBFM on a verified compatible handheld, using a LibreSDR reference station. The second radio is confirmed as a DM-1801 Pro, but its board revision and cable still need verification.

**Start here:** [`docs/DEVELOPMENT_PLAN.md`](docs/DEVELOPMENT_PLAN.md) and [`AGENTS.md`](AGENTS.md).

**Status:** The operator confirmed that the DM-1701 boots and works after installing Radioddity V02.03 CSV. Its menu reports `V002.003`. This is the tested stock fallback for this unit. M17 has not been tested on the radio. See the [arrival log](notes/arrival-session.md).

## Host-only quick start

From the checkout root, run with Python 3.8+ (use `python` on Windows).

```bash
python3 scripts/lab.py status
python3 -m unittest discover -s tests -v
```

See the [factory backup checklist](docs/factory-backup.md) and [LibreSDR host inventory](docs/libresdr-inventory.md) for next steps. Keep backup artifacts and unit identifiers outside this public repository.

**Next session:** Start with the [M17 development handoff](notes/next-session.md). Keep the first work on the computer, with no radio writes or transmissions.

**Upstream references:** <https://github.com/RadioFoundry/RadioFoundry>, <https://github.com/M17-Project/gr-m17>, <https://github.com/drowe67/radae>.
