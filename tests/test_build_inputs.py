"""Regression tests for build manifest consistency checks."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "verify-build-inputs.py"
SPEC = importlib.util.spec_from_file_location("verify_build_inputs", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class TestBuildInputs(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "port-source").mkdir()
        sources = {"recoil": {"revision": "a" * 40, "url": "https://example.invalid/recoil"}}
        assets = {"mesa": {"sha256": "b" * 64, "file": "mesa.tar.xz"}}
        for name, value in (("sources.lock.json", sources), ("assets.lock.json", assets)):
            for location in (self.root, self.root / "port-source"):
                (location / name).write_text(json.dumps(value), encoding="utf-8")

    def test_matching_manifests(self):
        self.assertEqual(MODULE.validate(self.root), [])

    def test_different_revisions_fail(self):
        file = self.root / "port-source" / "sources.lock.json"
        data = json.loads(file.read_text())
        data["recoil"]["revision"] = "c" * 40
        file.write_text(json.dumps(data))
        self.assertTrue(any("differ" in error for error in MODULE.validate(self.root)))

    def test_missing_manifest_fails(self):
        (self.root / "assets.lock.json").unlink()
        self.assertTrue(MODULE.validate(self.root))

    def test_invalid_checksum_fails(self):
        for location in (self.root, self.root / "port-source"):
            file = location / "assets.lock.json"
            file.write_text(json.dumps({"mesa": {"sha256": "invalid"}}))
        self.assertTrue(any("SHA-256" in error for error in MODULE.validate(self.root)))


if __name__ == "__main__":
    unittest.main()
