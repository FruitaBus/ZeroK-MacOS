# Contributing to Zero-K macOS

This is an **unofficial experimental Apple Silicon port**. Changes to the macOS port belong in this repository; upstream game and engine bugs should be triaged before filing with their respective maintainers.

## Pick a workstream

- **Build reproducibility:** make a fresh clone able to reproduce the published v0.1.0 application without developer-specific folders.
- **Recoil / save reliability:** investigate a repeatable Lua `newkey()` SIGSEGV after loading an active game save. The current loader patch is not a verified engine fix.
- **Chobby / packaging:** keep the version-name patch in the *active packaged* `Chobby-macos.sdz`, not only a loose directory.
- **Graphics:** commander previews, factory grounds/decals, and economy cable rendering.
- **Testing / docs:** clean-install validation, third-party source provenance, and automated smoke tests.

## First steps

1. Read [BUILD-FROM-SOURCE.md](BUILD-FROM-SOURCE.md) and [SOURCE-BUILD-NOTES.md](SOURCE-BUILD-NOTES.md).
2. Work on a branch, not the release tag or an installed `/Applications/Zero-K.app`.
3. Run `python3 scripts/preflight.py` to report missing prerequisites.
4. Run `python3 -m unittest discover -s tests -v` to test our Chobby patch tooling.
5. Open an issue with your environment, intended component, and how you will validate a change.

## Pull request expectations

Explain the root cause, the changed source, and the reproducible test. Include build instructions and regression coverage where practical. Do not upload credentials, player account data, private saves, crash reports containing identifiers, or redistributable proprietary assets without permission.

**Critical rule:** passing tests of tooling is not equivalent to validating a runnable `Zero-K.app`. Full reproducibility is pending an independent Apple Silicon build.

## Licensing

Preserve original authors' copyrights and component-specific licenses. See `LICENSE`, `notices/`, and source-build notes. Check corresponding-source obligations for distributed binaries and third-party assets before releases.
