#!/usr/bin/env python3
"""Verify root and nested build manifests agree before fetching/building.

Read-only: no downloads, source changes, or app modifications.
"""
import json
import sys
from pathlib import Path


def validate(root: Path) -> list[str]:
    errors = []
    for filename in ("sources.lock.json", "assets.lock.json"):
        files = [root / filename, root / "port-source" / filename]
        try:
            values = [json.loads(path.read_text(encoding="utf-8")) for path in files]
        except (OSError, ValueError) as exc:
            errors.append(f"{filename}: cannot load manifests: {exc}")
            continue
        if values[0] != values[1]:
            errors.append(f"{filename}: root and port-source manifests differ")
        if filename == "sources.lock.json":
            for name, entry in values[0].items():
                revision = entry.get("revision") if isinstance(entry, dict) else None
                if not isinstance(revision, str) or len(revision) != 40 or any(
                    c not in "0123456789abcdef" for c in revision.lower()
                ):
                    errors.append(f"{filename}: {name} has invalid commit SHA")
        else:
            for name, entry in values[0].items():
                checksum = entry.get("sha256") if isinstance(entry, dict) else None
                if not isinstance(checksum, str) or len(checksum) != 64 or any(
                    c not in "0123456789abcdef" for c in checksum.lower()
                ):
                    errors.append(f"{filename}: {name} has invalid SHA-256")
    return errors


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    errors = validate(root)
    if errors:
        for problem in errors:
            print(f"[FAIL] {problem}", file=sys.stderr)
        print("Build inputs inconsistent; stopping before fetch/build.", file=sys.stderr)
        return 1
    print("[OK] Root and port-source build manifests match and contain valid pins")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
