#!/usr/bin/env python3
"""Set the bundled Zero-K version in a Chobby SDZ archive."""

from pathlib import Path
import argparse
import os
import re
import tempfile
import zipfile

MEMBER = "LuaMenu/configs/gameConfig/zk/mainConfig.lua"
VERSION = "Zero-K v1.14.10.3"


def update_config(source):
    patterns = (
        (
            r'(_defaultGameArchiveName\s*=\s*)"[^"]*"',
            lambda m: m.group(1) + '"' + VERSION + '"',
        ),
        (
            r'(_defaultGameRapidTag\s*=\s*)(?:"[^"]*"|nil)',
            lambda m: m.group(1) + "nil",
        ),
    )

    for pattern, replacement in patterns:
        source, count = re.subn(pattern, replacement, source)

        if count != 1:
            raise RuntimeError(
                f"Expected exactly one configuration match: {pattern}"
            )

    return source


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()

    archive = args.archive.resolve()

    if not archive.is_file():
        raise SystemExit(f"Archive not found: {archive}")

    with zipfile.ZipFile(archive) as z:
        names = z.namelist()

        if names.count(MEMBER) != 1:
            raise SystemExit("Expected exactly one Chobby configuration member.")

        original = z.read(MEMBER).decode("utf-8")
        updated = update_config(original)

        if updated == original:
            print("Configuration already correct. No changes made.")
            return

        fd, temporary_name = tempfile.mkstemp(
            prefix="chobby-patch-",
            suffix=".sdz",
            dir=archive.parent,
        )
        os.close(fd)
        temporary = Path(temporary_name)

        try:
            with zipfile.ZipFile(temporary, "w") as out:
                for info in z.infolist():
                    data = (
                        updated.encode("utf-8")
                        if info.filename == MEMBER
                        else z.read(info)
                    )
                    out.writestr(info, data)

            with zipfile.ZipFile(temporary) as check:
                if check.testzip() is not None:
                    raise RuntimeError("Patched archive failed integrity check.")

                if check.read(MEMBER).decode("utf-8") != updated:
                    raise RuntimeError("Patched configuration verification failed.")

            os.replace(temporary, archive)
        finally:
            if temporary.exists():
                temporary.unlink()

    print("SUCCESS: Chobby archive configuration patched.")
    print("Game archive:", VERSION)
    print("Rapid tag: nil")


if __name__ == "__main__":
    main()
