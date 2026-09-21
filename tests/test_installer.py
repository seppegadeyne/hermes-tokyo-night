import importlib.util
from pathlib import Path
import tempfile
import unittest
spec = importlib.util.spec_from_file_location("installer", Path(__file__).parents[1] / "installer.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name)
        self.target, self.receipt = m.paths(self.home)

    def test_install_idempotence_and_uninstall(self):
        config = self.home / "config.yaml"
        config.write_text("display: {skin: another}\n")
        m.install(self.home)
        self.assertEqual(self.target.read_bytes(), m.ASSET.read_bytes())
        before = self.receipt.read_bytes()
        m.install(self.home)
        self.assertEqual(self.receipt.read_bytes(), before)
        m.uninstall(self.home)
        self.assertFalse(self.target.exists())
        self.assertFalse(self.receipt.exists())
        self.assertEqual(config.read_text(), "display: {skin: another}\n")
        m.uninstall(self.home)

    def test_collision_backup_restore(self):
        self.target.parent.mkdir()
        self.target.write_bytes(b"personal skin\n")
        with self.assertRaises(RuntimeError): m.install(self.home)
        m.install(self.home, replace=True)
        m.install(self.home)
        m.uninstall(self.home)
        self.assertEqual(self.target.read_bytes(), b"personal skin\n")

    def test_edits_survive(self):
        m.install(self.home)
        self.target.write_bytes(b"user edit")
        with self.assertRaises(RuntimeError): m.install(self.home, replace=True)
        with self.assertRaises(RuntimeError): m.uninstall(self.home)
        self.assertEqual(self.target.read_bytes(), b"user edit")

    def test_profile_isolation(self):
        other = self.home / "other"
        m.install(self.home)
        m.install(other)
        m.uninstall(self.home)
        self.assertEqual(m.paths(other)[0].read_bytes(), m.ASSET.read_bytes())

    def test_symlink_refused(self):
        self.target.parent.mkdir()
        self.target.symlink_to(self.home / "elsewhere")
        with self.assertRaises(RuntimeError): m.install(self.home, replace=True)
