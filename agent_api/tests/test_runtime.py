"""No-hardware process tests for execution isolation and completion semantics."""

import os
import tempfile
import time
import unittest
from pathlib import Path

from agent_api.runtime import ApiError, Runtime


FAKE_BRIDGE = r'''#!/usr/bin/env bash
set -eu
mode=$1
echo '{"event":"controller_start"}'
if [[ "$mode" == reset ]]; then
  echo '{"event":"reset_complete"}'
  echo '{"event":"outputs_stopped"}'
  exit 0
fi
trap 'echo "{\"event\":\"outputs_stopped\"}"; exit 130' TERM
if [[ "$*" == *"--duration 0.1"* ]]; then
  sleep 0.15
  echo '{"event":"inference_complete"}'
  echo '{"event":"outputs_stopped"}'
  exit 0
fi
while true; do sleep 0.05; done
'''


@unittest.skipUnless(os.name == "posix", "The deployment controller runs on Ubuntu")
class RuntimeProcessTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        script = root / "model_hardware_bridge" / "scripts" / "bridge.sh"
        script.parent.mkdir(parents=True)
        script.write_text(FAKE_BRIDGE, encoding="utf-8", newline="\n")
        script.chmod(0o755)
        self.runtime = Runtime(root=root, runs=root / "runs")
        self.addCleanup(self.runtime.close)
        self.runtime._hardware_ready = True

    def _start_fake_policy(self, execution_id, duration):
        with self.runtime._changed:
            record = self.runtime._new_record(execution_id, "policy", "pour_tea")
            self.runtime._start_bridge(record, "infer", ["--duration", str(duration)], "pour_tea")
        return record

    def _wait_terminal(self, record, timeout=3):
        deadline = time.monotonic() + timeout
        with self.runtime._changed:
            while record["state"] not in ("COMPLETED", "STOPPED", "TIMED_OUT", "FAILED"):
                remaining = deadline - time.monotonic()
                self.assertGreater(remaining, 0, "execution did not finish")
                self.runtime._changed.wait(timeout=remaining)
        return record

    def test_stop_targets_only_the_matching_policy_then_reset_can_run(self):
        policy = self._start_fake_policy("pour-1", 10)
        with self.assertRaises(ApiError) as wrong:
            self.runtime.stop_policy("pour-2")
        self.assertEqual(wrong.exception.code, "NOT_ACTIVE")
        self.assertIsNone(self.runtime._active.process.poll())
        self.assertTrue(self.runtime.stop_policy("pour-1")["accepted"])
        reset = self.runtime.reset_to_initial("reset-1", 2)
        self.assertEqual(self._wait_terminal(policy)["state"], "STOPPED")
        self.assertEqual(policy["stop_status"], "CONFIRMED")
        self.assertEqual(reset["state"], "COMPLETED")

    def test_duration_end_is_timeout_not_business_success(self):
        policy = self._start_fake_policy("pour-timeout", 0.1)
        self._wait_terminal(policy)
        self.assertEqual(policy["state"], "TIMED_OUT")
        self.assertIn("not inferred", policy["reason"])

    def test_execution_id_cannot_be_reused_for_another_operation(self):
        self._start_fake_policy("shared-id", 10)
        with self.assertRaises(ApiError) as duplicate:
            self.runtime.reset_to_initial("shared-id", 2)
        self.assertEqual(duplicate.exception.code, "DUPLICATE_EXECUTION_ID")
        self.runtime.stop_policy("shared-id")


if __name__ == "__main__":
    unittest.main()
