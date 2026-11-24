# Codex/agent instructions — ham-digital-modes-lab

Read `docs/DEVELOPMENT_PLAN.md` before making changes. Work in small, reviewable commits, with host-only tests first. This lab supports one DM-1701, one as-yet-unidentified DM-1801, a LibreSDR and a stock DR-1801UV.

## Critical restrictions

1. **No hardware-side actions without explicit human confirmation.** No flashing, bootloader erase, calibration writes, PTT/TX keying, RF gain/PA control, hardware probe that changes state, or raw serial control messages to a radio unless the user approves the exact command and device after safety checks.
2. Assume a Kenwood-shaped two-pin socket is *not* a generic TTL UART. The DM-1701 accessory connector uses native USB; the current DM-1801 Pro uses UART0 (115200 8N1) with PTT pin interaction. The arriving DM-1801 version is UNVERIFIED. Do not select images or cabling until confirmed.
3. Preserve all factory firmware, codeplugs, calibration, codec and actual radio identifiers **outside Git**. No copyrighted binary redistribution or log of private IDs.
4. Require RF containment: proper 50-ohm load, coupler/isolation, rated attenuator, verified power calculation and a human before transmitting; never feed RF power directly to an SDR input.
5. Distinguish source-verified capabilities, bench-verified results, simulation and hypothesis in docs and tests. Do not turn an unverified mode into a claim of support.
6. Keep M17 and RADE paths separate. M17 uses 4800-symbol/s 4FSK with Codec2 intended on-radio; RADE BBFM is external neural + 2400-symbol/s passband PSK through an FM audio/baseband path.
7. Handle code licensing consciously: RadioFoundry MIT versus GPL M17 reference projects, separately licensed Codec2 and RADE. Do not copy GPL code into MIT-targeted firmware. Do not commit stock AMBE/firmware images.
8. Always report commands run, tests passing/failing, modified files, and unresolved blockers. If hardware is absent, write clearly "NOT RUN ON HARDWARE".

## Priorities

Begin with the software-only, P0 tasks listed in `docs/DEVELOPMENT_PLAN.md`: inventory templates, backup checklist, UHD environment-detection script (read only), GNU Radio reference test instructions and RADE offline BER harness. Keep a Git commit for each independently testable step. The user should be able to run safe commands locally and paste outputs back. Do not make up a new firmware driver before receiving model/cable/backup evidence.

## Acceptance for every change

- Unit/host tests run; no radio required unless user separately opts in.
- Instructions reproducible on a fresh Linux machine, with version and hash records.
- Errors and uncertainty surfaced; no fake measurements or placeholder passes.
- Code for serial transport has simulated safety/timeouts and sample counters before opening a physical device.
- RF/flash commands deliberately excluded from automated tests and CI.
