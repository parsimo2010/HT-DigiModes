# Ham Digital Modes Lab — Codex starter

A research lab to develop standalone M17 on a Baofeng DM-1701 and host-assisted RADE BBFM on a verified compatible handheld, using a LibreSDR reference station. The second radio is confirmed as a DM-1801 Pro, but its board revision and cable still need verification.

**Start here:** [`docs/DEVELOPMENT_PLAN.md`](docs/DEVELOPMENT_PLAN.md) and [`AGENTS.md`](AGENTS.md).

**Status:** The operator confirmed basic analog FM and DMR transmit and receive on both handhelds before any firmware change. The DM-1701 stock codeplug was backed up privately. The updater completed an approved write of Radioddity V02.03 CSV to the DM-1701. First boot and operation on V02.03 are pending operator verification. See the [arrival log](notes/arrival-session.md).

## Host-only quick start

From the checkout root, run with Python 3.8+ (use `python` on Windows).

```bash
python3 scripts/lab.py status
python3 -m unittest discover -s tests -v
```

See the [factory backup checklist](docs/factory-backup.md) and [LibreSDR host inventory](docs/libresdr-inventory.md) for next steps. Keep backup artifacts and unit identifiers outside this public repository.

**For Codex:** Follow the first-session task in section 12 of the plan. Do software-only setup and testing, then request measured hardware facts. Do not claim the plan has been executed.

**Upstream references:** <https://github.com/RadioFoundry/RadioFoundry>, <https://github.com/M17-Project/gr-m17>, <https://github.com/drowe67/radae>.
