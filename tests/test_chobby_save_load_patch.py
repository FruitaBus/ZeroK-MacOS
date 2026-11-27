"""Run: python3 -m unittest discover -s tests -v"""
import importlib.util
import tempfile
import unittest
import zipfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / 'scripts/patch-chobby-save-load.py'
spec = importlib.util.spec_from_file_location('patch_chobby_save_load', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class TestChobbyPatch(unittest.TestCase):
    def test_versions_and_zip_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            src, dest = Path(tmp)/'old.sdz', Path(tmp)/'new.sdz'
            old = b'prefix\n' + module.OLD + b'\nsuffix\n'
            with zipfile.ZipFile(src, 'w') as z:
                z.writestr(module.MEMBER, old)
                z.writestr('test.txt', b'untouched')
            module.run(src, dest, False)
            self.assertFalse(dest.exists())
            module.run(src, dest, True)
            with zipfile.ZipFile(dest) as z:
                self.assertIn(module.MARKER, z.read(module.MEMBER))
                self.assertNotIn(module.OLD, z.read(module.MEMBER))
                self.assertEqual(z.read('test.txt'), b'untouched')
            with self.assertRaises(FileExistsError):
                module.run(src, dest, True)

    def test_refuses_unknown_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            src, dest = Path(tmp)/'old.sdz', Path(tmp)/'new.sdz'
            with zipfile.ZipFile(src, 'w') as z:
                z.writestr(module.MEMBER, 'unexpected contents')
            with self.assertRaises(ValueError):
                module.run(src, dest, True)
            self.assertFalse(dest.exists())

    def test_refuses_modifying_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp)/'old.sdz'
            with zipfile.ZipFile(src, 'w') as z:
                z.writestr(module.MEMBER, module.OLD)
            with self.assertRaises(ValueError):
                module.run(src, src, True)


if __name__ == '__main__':
    unittest.main()
