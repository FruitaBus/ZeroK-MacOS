#!/usr/bin/env python3
"""Non-destructive host/repository preflight for ZeroK-MacOS.
Run from a repository checkout: python3 scripts/preflight.py
"""
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def emit(label, state, detail):
    print(f"[{state:4}] {label:25} {detail}")


def main():
    errors = 0
    system, machine = platform.system(), platform.machine()
    emit("Host", "INFO", f"{system} {machine} ({platform.release()})")
    if system != "Darwin" or machine != "arm64":
        emit("Apple Silicon", "WARN", "Native builds require an Apple Silicon Mac; auditing still works elsewhere")
    for name in ("python3", "git", "cmake", "ninja", "brew", "pkg-config", "uv", "dotnet", "meson", "ccache", "codesign", "otool", "install_name_tool"):
        path = shutil.which(name)
        emit(name, "OK" if path else "MISS", path or "not found")
        if not path and name in {"git", "cmake", "ninja", "uv", "dotnet"}:
            errors += 1
    if system == "Darwin":
        try:
            proc = subprocess.run(["xcode-select", "-p"], capture_output=True, text=True, timeout=10)
            emit("Xcode developer path", "OK" if proc.returncode == 0 else "MISS", proc.stdout.strip() or proc.stderr.strip())
        except (OSError, subprocess.TimeoutExpired):
            emit("Xcode developer path", "MISS", "xcode-select unavailable")
    locks = {}
    for filename in ("sources.lock.json", "assets.lock.json"):
        path = ROOT / filename
        try:
            locks[filename] = json.loads(path.read_text())
            emit(filename, "OK", f"{len(locks[filename])} entries")
        except (OSError, ValueError) as exc:
            emit(filename, "FAIL", str(exc)); errors += 1
    for directory in ("port-source", "release-patches", "modified-recoil", "packaged-game-config"):
        emit(directory, "OK" if (ROOT / directory).exists() else "MISS", str(ROOT / directory))
        if not (ROOT / directory).exists(): errors += 1
    for filename in ("release-patches/recoil-lua-save-fix.patch", "release-patches/patch-chobby-version.py", "port-source/scripts/build-app.sh"):
        emit(filename, "OK" if (ROOT / filename).is_file() else "MISS", str(ROOT / filename))
        if not (ROOT / filename).is_file(): errors += 1
    if 'sources.lock.json' in locks:
        for name, entry in locks['sources.lock.json'].items():
            revision = entry.get('revision', '')
            emit(f"source {name}", "OK" if len(revision) == 40 and all(c in '0123456789abcdef' for c in revision.lower()) else "WARN", revision)
    if 'assets.lock.json' in locks:
        for name, entry in locks['assets.lock.json'].items():
            sha = entry.get('sha256', '')
            if len(sha) != 64 or any(c not in '0123456789abcdef' for c in sha.lower()):
                emit(f"asset {name}", "FAIL", "missing/invalid SHA-256"); errors += 1
    if system == 'Darwin':
        free = shutil.disk_usage(str(ROOT)).free / (1024**3)
        emit("Free disk", "INFO", f"{free:.1f} GiB (full native build needs substantial space)")
    print("\nPASS: basic preflight" if errors == 0 else f"\nINCOMPLETE: {errors} required checks failed; do not start a full build yet")
    return int(errors != 0)


if __name__ == "__main__":
    sys.exit(main())
