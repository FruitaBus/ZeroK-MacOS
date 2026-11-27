# Integration instructions for repository maintainer

This ZIP is an **additive contribution kit**, not an entire Git checkout and not a working build artifact.

1. Use the local repository checkout: `~/Downloads/ZeroK-Release-0.1.0/github-source` (or a fresh clone).
2. Extract the ZIP **into the checkout root**, preserving the `scripts/`, `tests/`, `docs/` paths. The kit does not overwrite the current `README.md`, `SOURCE-BUILD-NOTES.md`, or release patches.
3. Review the diff: `git status --short` and `git diff --no-index /dev/null scripts/preflight.py` (similar for each new file) or simply inspect them in your editor.
4. Run `python3 -m unittest discover -s tests -v`, then `python3 scripts/preflight.py` on Apple Silicon.
5. Update the main README with links to `BUILD-FROM-SOURCE.md`, `CONTRIBUTING.md`, and `BUILD-REPRODUCIBILITY-TRACKER.md`.
6. Make a new branch, commit and open a PR. Do not run `build-app.sh` during this step.

These files do not change `Zero-K.app`, save files, the v0.1.0 DMG or existing source patches.
