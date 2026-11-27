#!/usr/bin/env python3
"""Apply the save-version name fix to a standalone Chobby .sdz archive.
Safe defaults: dry-run unless --apply; no in-place archive changes; SHA-256 audit.
Does not modify user saves, the installed app, or the public release.
"""
import argparse
import hashlib
import sys
import zipfile
from pathlib import Path

MEMBER = 'LuaMenu/widgets/gui_loadgame.lua'
OLD = b'local game = saveData.gameName .. " " .. saveData.gameVersion'
NEW = (b'local game = saveData.gameName\n'
       b'\tlocal suffix = " " .. saveData.gameVersion\n'
       b'\tif not VFS.HasArchive(game) and game:sub(-#suffix) ~= suffix then\n'
       b'\t\tgame = game .. suffix\n'
       b'\tend')
MARKER = b'game:sub(-#suffix) ~= suffix'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def run(src, dest, apply):
    if not src.is_file() or not zipfile.is_zipfile(src):
        raise ValueError('Input must be an existing ZIP-compatible Chobby .sdz archive')
    if src.resolve() == dest.resolve():
        raise ValueError('Refusing in-place modification; choose a separate output path')
    with zipfile.ZipFile(src) as z:
        names = z.namelist()
        if names.count(MEMBER) != 1:
            raise ValueError(f'Expected exactly one {MEMBER}, found {names.count(MEMBER)}')
        original = z.read(MEMBER)
        if original.count(OLD) == 1:
            changed = original.replace(OLD, NEW, 1)
            status = 'requires patch'
        elif OLD not in original and MARKER in original:
            changed = original
            status = 'already patched'
        else:
            raise ValueError('Unexpected source layout: manual review required; no output written')
        print(f'Input:        {src}')
        print(f'Lua member:   {MEMBER}')
        print(f'Existing SHA: {digest(original)}')
        print(f'Patched SHA:  {digest(changed)}')
        print(f'Status:       {status}')
        if not apply:
            print('DRY RUN: nothing changed; add --apply and --output PATH to create patched archive')
            return
        if dest.exists():
            raise FileExistsError(f'Output exists; refusing overwrite: {dest}')
        dest.parent.mkdir(parents=True, exist_ok=True)
        try:
            with zipfile.ZipFile(dest, 'w') as out:
                out.comment = z.comment
                for member in z.infolist():
                    data = changed if member.filename == MEMBER else z.read(member)
                    out.writestr(member, data)
            with zipfile.ZipFile(dest) as check:
                bad = check.testzip()
                if bad or check.read(MEMBER) != changed:
                    raise ValueError(f'Output archive verification failed: {bad}')
            print(f'Created:      {dest}')
        except BaseException:
            dest.unlink(missing_ok=True)
            raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--output', type=Path, help='Required when using --apply; output cannot already exist')
    args = parser.parse_args()
    if args.apply and args.output is None:
        parser.error('--output is required with --apply')
    try:
        run(args.archive, args.output or args.archive.with_suffix('.patched.sdz'), args.apply)
    except (ValueError, OSError, zipfile.BadZipFile) as exc:
        parser.exit(2, f'ERROR: {exc}\n')


if __name__ == '__main__':
    main()
