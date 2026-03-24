import unittest
from types import SimpleNamespace

from core.mouse_hook import _supports_global_remap_device


class MouseHookDeviceFilterTests(unittest.TestCase):
    def test_accepts_master_3_series_devices(self):
        self.assertTrue(_supports_global_remap_device(SimpleNamespace(key="mx_master_3")))
        self.assertTrue(_supports_global_remap_device(SimpleNamespace(key="mx_master_3s")))

    def test_rejects_non_master_3_devices(self):
        self.assertFalse(_supports_global_remap_device(SimpleNamespace(key="mx_master_2s")))
        self.assertFalse(_supports_global_remap_device(SimpleNamespace(key="magic_trackpad")))
        self.assertFalse(_supports_global_remap_device(SimpleNamespace(key="")))
        self.assertFalse(_supports_global_remap_device(SimpleNamespace()))


if __name__ == "__main__":
    unittest.main()
