import contextlib
import io
import subprocess
import unittest
from unittest.mock import call, patch

from scripts import lab


class StatusTests(unittest.TestCase):
    @patch("scripts.lab.subprocess.run")
    @patch("scripts.lab.shutil.which", return_value=None)
    def test_missing_tools_do_not_launch_processes(self, which, run):
        self.assertEqual(lab.tool_status("uhd_config_info", True), "not on PATH")
        run.assert_not_called()

    @patch("scripts.lab.subprocess.run")
    @patch("scripts.lab.shutil.which", side_effect=lambda name: name)
    def test_only_version_commands_are_launched(self, which, run):
        run.return_value = subprocess.CompletedProcess([], 0, "test-version\n", "")
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            lab.status()
        kwargs = dict(capture_output=True, encoding="utf-8", errors="replace",
                      timeout=5, check=False)
        self.assertEqual(run.call_args_list, [
            call(["uhd_config_info", "--version"], **kwargs),
            call(["gnuradio-config-info", "--version"], **kwargs),
        ])
        self.assertIn("uhd_usrp_probe: available (not run)", output.getvalue())
        self.assertIn("uhd_find_devices: available (not run)", output.getvalue())

    @patch("scripts.lab.subprocess.run", side_effect=subprocess.TimeoutExpired("tool", 5))
    @patch("scripts.lab.shutil.which", return_value="tool")
    def test_timeouts_are_reported(self, which, run):
        self.assertEqual(lab.tool_status("tool", True), "version check timed out")

    @patch("scripts.lab.subprocess.run", return_value=subprocess.CompletedProcess([], 2, "", ""))
    @patch("scripts.lab.shutil.which", return_value="tool")
    def test_failed_version_query_is_reported(self, which, run):
        self.assertEqual(lab.tool_status("tool", True), "version check failed (exit 2)")
