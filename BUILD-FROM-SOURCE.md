# Build Zero-K macOS from source: contributor guide (in progress)

**Current status: partial build workflow, NOT a verified clean-room reconstruction of v0.1.0.** This page deliberately distinguishes validated tooling from unverified native build steps.

## Target

- Apple Silicon (ARM64), macOS 26 or later.
- Zero-K game v1.14.10.3, Recoil 2026.07.04 for the published v0.1.0 snapshot.
- Published source pins: `sources.lock.json`; asset SHA-256 checks: `assets.lock.json`.

## Recommended first run

```bash
git clone https://github.com/FruitaBus/ZeroK-MacOS.git
cd ZeroK-MacOS
python3 scripts/preflight.py
python3 -m unittest discover -s tests -v
```

If `scripts/preflight.py` is absent, the contributor-preparation changes have not yet been merged. It reports missing tools but **does not install anything**.

## Build inputs and dependencies

The existing `port-source/scripts/build-app.sh` expects tools such as Homebrew, `uv`, CMake, Ninja, GCC 16, .NET, Mesa's build tools, and Apple's developer utilities. See its source to resolve package versions. **Do not assume the current host tools or binary dependencies are compatible merely because preflight passes.**

The repository records external Recoil, Chobby, and Infrastructure source revisions in `sources.lock.json`. The `port-source` build script expects checkouts in its own `external/` directory and lockfiles/assets relative to `port-source/`. Before running it, confirm that it can see the published top-level lockfiles and release patches. Do not fix those path mismatches by silently copying versioned assets into an installed game.

## Recoil source

The recorded Recoil fork revision is `199b752a79f5c9211d88986c98bef1482ea2f1f9`. The v0.1.0 snapshot includes `release-patches/recoil-lua-save-fix.patch` and full copies of the three edited files. See `SOURCE-BUILD-NOTES.md` for the upstream acquisition and patch sequence. The save/load patch has known unresolved stability problems with some active battle saves; treat it as **historical release source**, not a verified general save/load fix.

## Chobby source

The published `release-patches/patch-chobby-version.py` changes Chobby's configured game version, but it does **not** repair the save-loader script. To inspect and produce a *new* archive with that separate correction:

```bash
python3 scripts/patch-chobby-save-load.py path/to/Chobby-macos.sdz
python3 scripts/patch-chobby-save-load.py path/to/Chobby-macos.sdz --apply --output /tmp/Chobby-macos-patched.sdz
```

The script preserves other archive entries and refuses in-place changes and unrecognized source layouts. It is a development tool; it does **not** independently rebuild the whole Chobby archive or prove full game loading is reliable.

## Existing upstream pipeline (advanced; not yet clean-room validated)

The existing build process is `port-source/scripts/build-app.sh`, which:

1. Fetches pinned external source checkouts and checksum-verified assets.
2. Builds Mesa/Zink graphics components.
3. Configures and builds the native Recoil engine and AI modules.
4. Builds the Chobby client and .NET launcher helper.
5. Packages and audits an app.

**Do not run it on a valuable checkout before reviewing it.** It writes build outputs and a `dist/Zero-K.app` directory. It currently does not automatically apply the published release patches or reproduce all standalone dependency relinking and packaging differences. For the published release, refer to `SOURCE-BUILD-NOTES.md`.

## Definition of a reproducible build

A contributor starting from a fresh checkout on a separate Apple Silicon Mac must be able to download all licensed inputs, verify hashes/revisions, build and relink dependencies, create an app and DMG, and pass architecture, library dependency, signature, clean install, new game, and saved game tests. Publish the exact command sequence and output provenance. Until then, describe the project as **buildable in parts**, not one-command reproducible.

## Known gaps for contributors

- Lockfiles and patch application aren't yet integrated end-to-end with the nested `port-source` pipeline.
- Standalone Mesa/Zink/KosmicKrisp binaries, build configs, license review and dylib relinking require reconciliation.
- Corrected Chobby packaging must become part of the build, not a manual final step.
- The app's original binary SHA-256 is a provenance marker, not a guarantee of byte-for-byte identical rebuilt binaries.
- No independent clean Mac build is recorded.

See [BUILD-REPRODUCIBILITY-TRACKER.md](BUILD-REPRODUCIBILITY-TRACKER.md) for handoff tasks.
