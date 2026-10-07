# Regression tests for issue #2: logging on a new platform must appear in totals.
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import earnings


class LogCreatesPlatformTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self._orig = earnings.DATA_FILE
        earnings.DATA_FILE = os.path.join(self.tmp.name, "earnings.json")

    def tearDown(self):
        earnings.DATA_FILE = self._orig
        self.tmp.cleanup()

    def test_log_new_platform_is_created_and_counted(self):
        earnings.cmd_log(["test-platform", "5", "test payout"])
        data = earnings.load_data()
        self.assertIn("test-platform", data["platforms"])
        self.assertEqual(data["platforms"]["test-platform"]["total_earned"], 5.0)

    def test_log_existing_platform_accumulates(self):
        earnings.cmd_add(["ugig"])
        earnings.cmd_log(["ugig", "3", "first"])
        earnings.cmd_log(["ugig", "2", "second"])
        data = earnings.load_data()
        self.assertEqual(data["platforms"]["ugig"]["total_earned"], 5.0)


if __name__ == "__main__":
    unittest.main()
