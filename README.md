# Ham Digital Modes Lab — Codex starter

A research lab to develop standalone M17 on a Baofeng DM-1701 and host-assisted RADE BBFM on a verified compatible handheld, using a LibreSDR reference station. The incoming "DM-1801" hardware revision must be identified before any firmware or cable decisions.

**Start here:** [`docs/DEVELOPMENT_PLAN.md`](docs/DEVELOPMENT_PLAN.md) and [`AGENTS.md`](AGENTS.md).

**Status:** Starter scaffolding. Windows enumerated the DM-1701 over USB, but no radio protocol, RF, or flash tests have been run. See the [arrival log](notes/arrival-session.md).

## Host-only quick start

From the checkout root, run with Python 3.8+ (use `python` on Windows).

```bash
python3 scripts/lab.py status
python3 -m unittest discover -s tests -v
```

See the [factory backup checklist](docs/factory-backup.md) and [LibreSDR host inventory](docs/libresdr-inventory.md) for next steps. Keep backup artifacts and unit identifiers outside this public repository.

**For Codex:** Follow the first-session task in section 12 of the plan. Do software-only setup and testing, then request measured hardware facts. Do not claim the plan has been executed.

**Upstream references:** <https://github.com/RadioFoundry/RadioFoundry>, <https://github.com/M17-Project/gr-m17>, <https://github.com/drowe67/radae>.
