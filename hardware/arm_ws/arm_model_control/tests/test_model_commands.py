import math
import unittest

from arm_model_control.model_commands import JOINT_NAMES, ModelCommandError, ModelCommandGate


class ModelCommandGateTest(unittest.TestCase):
    def setUp(self):
        self.gate = ModelCommandGate([-180] * 6, [180] * 6)
        self.gate.enable(100_000_000_000, 10.0)

    def accept(self, positions=None, names=JOINT_NAMES, stamp_ns=100_010_000_000,
               now_ns=100_010_000_000, now_monotonic=10.01, current_deg=None):
        return self.gate.accept(
            names, positions if positions is not None else [0.01] * 6 + [0.0],
            stamp_ns, now_ns=now_ns, now_monotonic=now_monotonic,
            current_deg=current_deg if current_deg is not None else [0.0] * 6)

    def test_reorders_names_converts_radians_and_excludes_padding(self):
        values = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.0]
        out = self.accept(list(reversed(values)), tuple(reversed(JOINT_NAMES)))
        self.assertEqual(len(out), 6)
        for actual, value in zip(out, values):
            self.assertAlmostEqual(actual, math.degrees(value))

    def test_rejects_missing_duplicate_or_unknown_names(self):
        for names in (JOINT_NAMES[:6], ("joint1",) * 7,
                      tuple(f"left_joint{i}" for i in range(1, 8))):
            with self.subTest(names=names), self.assertRaises(ModelCommandError):
                self.accept(names=names)

    def test_rejects_length_nonfinite_and_nonzero_padding(self):
        for q in ([0.0] * 6, [0.0] * 8, [float("nan")] + [0.0] * 6,
                  [float("inf")] + [0.0] * 6, [0.0] * 6 + [0.01]):
            with self.subTest(q=q), self.assertRaises(ModelCommandError):
                self.accept(q)

    def test_rejects_joint_limits(self):
        with self.assertRaisesRegex(ModelCommandError, "outside limits"):
            self.accept([math.pi + 0.01] + [0.0] * 6,
                        current_deg=[180.0] + [0.0] * 5)

    def test_rejects_large_absolute_jump(self):
        with self.assertRaisesRegex(ModelCommandError, "jump"):
            self.accept([0.21] + [0.0] * 6)

    def test_multiturn_joint_is_not_silently_wrapped(self):
        self.gate = ModelCommandGate([-360] * 6, [360] * 6)
        self.gate.enable(100_000_000_000, 10.0)
        with self.assertRaisesRegex(ModelCommandError, "jump"):
            self.accept([0.0] * 6 + [0.0], current_deg=[0.0] * 5 + [359.0])

    def test_rejects_pre_enable_duplicate_stale_and_future_timestamps(self):
        for stamp, now in ((0, 100_010_000_000),
                           (100_000_000_000, 100_010_000_000),
                           (100_010_000_000, 100_400_000_000),
                           (100_100_000_000, 100_010_000_000)):
            with self.subTest(stamp=stamp, now=now), self.assertRaises(ModelCommandError):
                self.accept(stamp_ns=stamp, now_ns=now)
        self.accept()
        with self.assertRaisesRegex(ModelCommandError, "duplicated/out of order"):
            self.accept()

    def test_invalid_input_does_not_refresh_watchdog(self):
        self.accept()
        with self.assertRaises(ModelCommandError):
            self.accept([float("nan")] * 7, stamp_ns=100_020_000_000,
                        now_ns=100_020_000_000, now_monotonic=10.02)
        self.assertAlmostEqual(self.gate.last_receive_monotonic, 10.01)

    def test_startup_grace_then_normal_timeout(self):
        self.assertFalse(self.gate.expired(19.99))
        self.assertTrue(self.gate.expired(20.01))
        self.accept()
        self.assertFalse(self.gate.expired(10.30))
        self.assertTrue(self.gate.expired(10.32))
        with self.assertRaisesRegex(ModelCommandError, "timed out"):
            self.accept(stamp_ns=100_400_000_000, now_ns=100_400_000_000,
                        now_monotonic=10.4)

    def test_disabled_and_new_session_reject_old_targets(self):
        old_generation = self.gate.generation
        self.gate.disable()
        self.assertNotEqual(old_generation, self.gate.generation)
        with self.assertRaisesRegex(ModelCommandError, "disabled"):
            self.accept()
        self.gate.enable(101_000_000_000, 11.0)
        with self.assertRaises(ModelCommandError):
            self.accept(now_ns=101_010_000_000, now_monotonic=11.01)

    def test_configuration_must_describe_six_real_joints(self):
        with self.assertRaises(ValueError):
            ModelCommandGate([-180] * 7, [180] * 7)
        for kwargs in ({"timeout_sec": 0}, {"max_delta_rad": float("nan")},
                       {"padding_tolerance_rad": -1}, {"first_command_timeout_sec": 0}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                ModelCommandGate([-180] * 6, [180] * 6, **kwargs)


if __name__ == "__main__":
    unittest.main()
