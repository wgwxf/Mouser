import unittest
from types import SimpleNamespace

from core.mouse_hook import _supports_global_remap_device


class MouseHookDeviceFilterTests(unittest.TestCase):
    def test_accepts_mx_master_family_devices(self):
        self.assertTrue(_supports_global_remap_device(SimpleNamespace(key="mx_master")))
        self.assertTrue(_supports_global_remap_device(SimpleNamespace(key="mx_master_2s")))
        self.assertTrue(_supports_global_remap_device(SimpleNamespace(key="mx_master_3")))
        self.assertTrue(_supports_global_remap_device(SimpleNamespace(key="mx_master_3s")))

    def test_accepts_receiver_backed_devices(self):
        self.assertTrue(_supports_global_remap_device(SimpleNamespace(key="usb_receiver")))
        self.assertTrue(_supports_global_remap_device(SimpleNamespace(key="bolt_receiver")))

    def test_rejects_non_mx_master_devices(self):
        self.assertFalse(_supports_global_remap_device(SimpleNamespace(key="magic_trackpad")))
        self.assertFalse(_supports_global_remap_device(SimpleNamespace(key="mx_anywhere_3s")))
        self.assertFalse(_supports_global_remap_device(SimpleNamespace(key="")))
        self.assertFalse(_supports_global_remap_device(SimpleNamespace()))


if __name__ == "__main__":
    unittest.main()
