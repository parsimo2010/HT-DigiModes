"""Host-only lab commands. Never opens or enumerates physical devices."""

import argparse
import platform
import shutil
import subprocess


def tool_status(name, version=False):
    path = shutil.which(name)
    if path is None:
        return "not on PATH"
    if not version:
        return "available (not run)"
    try:
        result = subprocess.run(
            [path, "--version"], capture_output=True, encoding="utf-8",
            errors="replace", timeout=5, check=False,
        )
    except subprocess.TimeoutExpired:
        return "version check timed out"
    except OSError as exc:
        return f"version check failed ({exc.strerror or type(exc).__name__})"
    if result.returncode:
        return f"version check failed (exit {result.returncode})"
    lines = (result.stdout.strip() or result.stderr.strip()).splitlines()
    return lines[0] if lines else "version check returned no output"


def status():
    print(f"Host: {platform.system()} {platform.machine()}")
    print(f"Python: {platform.python_version()}")
    for name, version in (
        ("uhd_config_info", True),
        ("gnuradio-config-info", True),
        ("uhd_find_devices", False),
        ("uhd_usrp_probe", False),
    ):
        print(f"{name}: {tool_status(name, version)}")
    print("No hardware discovery or probe was run.")


def main():
    parser = argparse.ArgumentParser(prog="lab", description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("status", help="report local tool availability and versions")
    parser.parse_args()
    status()


if __name__ == "__main__":
    main()
