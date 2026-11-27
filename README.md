# Zero-K macOS 0.1.0 — unofficial preview source

This repository is the **source and patch reference kit** for a tested standalone
Apple Silicon build of Zero-K, **not an official Zero-K project release**.

_Mini Patch 11-27-26: I expanded the Zero-K macOS GitHub repository with new build documentation, contributor guidelines, prerequisite checks, Chobby save-loading patch tools, and automated regression tests. These additions make it easier for developers to explore the source code, contribute improvements, and work toward building the game independently on Apple Silicon Macs._

# Contributions and collaboration are welcome!

[Download DMG for MacOS](https://github.com/FruitaBus/ZeroK-MacOS/releases/download/v0.1.0/Zero-K-0.1.0-arm64-TEST.dmg)

As expected, since this isn't a "licensed" game, you'll get the security popup upon first launch. Select cancel, go to Settings>Privacy & Security, scroll down and click Open Anyway for Zero-K.


- Platform: Apple Silicon (ARM64), macOS 26 or newer
- Game: Zero-K v1.14.10.3; Recoil 2026.07.04
- Application: org.zerok.macos, version 0.1.0
- Tested binary DMG SHA-256: `b7e5cc0282b996916a732d58108686975d75a22bbb8af9a3348fc962f49481fb`
- Tested `spring` SHA-256: `0d6f38583ae50190c6abbe59b7637b11578516e0de909e0c0962fc25114c4b66`

## Contents

- `port-source/`: tracked ZkMacOS build, launcher, patch, test and documentation files
- `release-patches/recoil-lua-save-fix.patch`: exact 3-file Recoil source diff
- `modified-recoil/`: full copies of the three modified Recoil source files
- `release-patches/patch-chobby-version.py`: correct bundled Chobby game version
- `packaged-game-config/`: actual production Chobby config and Zero-K modinfo
- `sources.lock.json` and `assets.lock.json`: pinned upstream sources and dependencies
- `notices/` and `LICENSE`: applicable bundled notices and GPL text
- `SOURCE-BUILD-NOTES.md`: source acquisition and patch guidance
- [`BUILD-FROM-SOURCE.md`](BUILD-FROM-SOURCE.md): contributor setup, tested checks, and known limitations
- [`CONTRIBUTING.md`](CONTRIBUTING.md): contribution and development guidelines
- `RELEASE-CHECKLIST.md`: required manual checks before public distribution

The working binary was built separately and tested locally (AI play, saves, reloads,
DMG integrity and an installation outside the build tree). These tests do not prove
multiplayer compatibility, broad hardware support, or complete source reproducibility.

**Important:** The existing upstream `port-source/scripts/build-app.sh` is NOT a one-click
rebuild of this exact tested binary. It can rebuild/overwrite the packaged app and
it does not automatically apply the additional release patches. Follow the build
notes and reconcile the packaging steps before claiming reproducible full builds.

No account data, replays, user saves, compiled app, or 2 GB DMG is committed here.

For credits and license terms, see `notices/THIRD-PARTY.md`. Review Valve's separate
Steam API terms and corresponding-source obligations before public distribution.
