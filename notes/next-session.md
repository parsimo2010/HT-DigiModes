# DM-1701 M17 development handoff

**Current status.** The operator has completed the first on-air DM-1701 M17 data test. The earlier preparation record follows. [Hardware result and factory backup](dm1701-m17-first-rf.md).

The DM-1701 runs Radioddity V02.03 CSV and the operator confirmed normal operation. The menu shows `V002.003`. This is the stock firmware we can return to through the tested USB update route. The previous `D012.006` installation was not dumped. The channel backup exists, but retaining the channels for M17 is not a requirement.

Read [AGENTS.md](../AGENTS.md), the [development plan](../docs/DEVELOPMENT_PLAN.md), and the [arrival log](arrival-session.md). Use the [pinned upstream revisions](upstream-lock.md). Firmware files and backups are private and outside Git.

1. **Run M17 entirely on the computer.** Start with the GNU Radio reference loopback (`LAB-004`). Record tool versions and a decoded frame result. Save reference frame bits and symbols for tests (`M17-001`). No radio or SDR is needed for the loopback.
2. **Build the DM-1701 baseline without installing it.** Build the pinned RadioFoundry target, run its host tests, and record the output checksum (`LAB-009`). Start the M17 implementation against those tests and reference vectors. M17 has not yet run on this radio.
3. **Prepare the first bench test separately.** Complete the applicable lab gates, including the SDR setup and a safe RF test fixture. Before requesting approval for a new flash, preview exactly which parts of memory will be changed. The bootloader and factory calibration must stay untouched. Factory calibration has not been copied out yet. If the approved firmware can read it after the first boot, save it privately before changing settings or testing RF.

Keep the DM-1801 Pro and RADE as a separate track. The authorization used for the stock update does not authorize a new flash or an RF test.
