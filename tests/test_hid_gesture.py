import unittest

from core import hid_gesture


class HidBackendPreferenceTests(unittest.TestCase):
    def test_default_backend_uses_iokit_on_macos(self):
        self.assertEqual(hid_gesture._default_backend_preference("darwin"), "iokit")

    def test_default_backend_uses_auto_elsewhere(self):
        self.assertEqual(hid_gesture._default_backend_preference("win32"), "auto")
        self.assertEqual(hid_gesture._default_backend_preference("linux"), "auto")


class GestureCandidateSelectionTests(unittest.TestCase):
    def test_choose_gesture_candidates_prefers_known_device_cids(self):
        listener = hid_gesture.HidGestureListener()
        device_spec = hid_gesture.resolve_device(product_id=0xB023)

        candidates = listener._choose_gesture_candidates(
            [
                {"cid": 0x00D7, "flags": 0x03B0, "mapping_flags": 0x0051},
                {"cid": 0x00C3, "flags": 0x0130, "mapping_flags": 0x0011},
            ],
            device_spec=device_spec,
        )

        self.assertEqual(candidates[:2], [0x00C3, 0x00D7])

    def test_choose_gesture_candidates_uses_capability_heuristic(self):
        listener = hid_gesture.HidGestureListener()

        candidates = listener._choose_gesture_candidates(
            [
                {"cid": 0x00A0, "flags": 0x0030, "mapping_flags": 0x0001},
                {"cid": 0x00F1, "flags": 0x01B0, "mapping_flags": 0x0011},
            ],
        )

        self.assertEqual(candidates[0], 0x00F1)

    def test_choose_gesture_candidates_falls_back_to_defaults(self):
        listener = hid_gesture.HidGestureListener()

        self.assertEqual(
            listener._choose_gesture_candidates([]),
            list(hid_gesture.DEFAULT_GESTURE_CIDS),
        )


class GestureReportHandlingTests(unittest.TestCase):
    def test_on_report_accepts_any_gesture_candidate_cid(self):
        events = []
        listener = hid_gesture.HidGestureListener(
            on_down=lambda: events.append("down"),
            on_up=lambda: events.append("up"),
        )
        listener._feat_idx = 0x05
        listener._gesture_cid = 0x00C3
        listener._gesture_candidates = [0x00C3, 0x00D7]
        listener._gesture_report_cids = set(listener._gesture_candidates)

        listener._on_report([hid_gesture.SHORT_ID, 0xFF, 0x05, hid_gesture.MY_SW, 0x00, 0xD7, 0x00, 0x00])
        listener._on_report([hid_gesture.SHORT_ID, 0xFF, 0x05, hid_gesture.MY_SW, 0x00, 0x00])

        self.assertEqual(events, ["down", "up"])


if __name__ == "__main__":
    unittest.main()
