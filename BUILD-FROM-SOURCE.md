# Build Zero-K for macOS

This is an **unofficial experimental Apple Silicon port** of Zero-K. The published v0.1.0 app targets **macOS 26 or newer**.

**Before you start:** The source is public, but building the exact released app from a fresh clone is **not yet verified**. The existing build script is a starting point for developers, not a guaranteed one-command reproduction of the downloadable DMG.

## 1. Get the source

Open Terminal on an Apple Silicon Mac:

```bash
git clone https://github.com/FruitaBus/ZeroK-MacOS.git
cd ZeroK-MacOS
```

## 2. Check your Mac

You will need Xcode and its command-line tools, Homebrew, Python 3, Git, CMake, Ninja, GCC 16, `.NET`, `uv`, and the graphics build tools used by Mesa. The build also calls `msbuild`; see the existing build scripts if that command is missing.

Run the included checker:

```bash
python3 scripts/preflight.py
```

It lists tools it can find and reports missing essentials. **It does not install anything**, and a passing check does not guarantee a complete build.

If you want to check the included contributor tests:

```bash
python3 -m unittest discover -s tests -v
```

## 3. Try the existing build

Use a **fresh, disposable checkout** rather than your installed game or a valuable development folder. The build downloads external sources and dependencies, compiles native libraries, and writes output inside `port-source/`.

```bash
cd port-source
bash scripts/build-app.sh
```

If the build completes, its application output is expected at:

```text
port-source/dist/Zero-K.app
```

The script's final audit is useful, but it does **not** prove the app exactly matches the released v0.1.0 DMG.

## 4. If it doesn't build

Please open a [GitHub issue](https://github.com/FruitaBus/ZeroK-MacOS/issues) with your macOS version, Mac model, the command you ran, and the **first relevant error message** (remove personal details and credentials). Build help and improvements are welcome.

## Important notes for contributors

- The build uses source versions recorded in `sources.lock.json` and dependencies recorded in `assets.lock.json`.
- The repository also includes `release-patches/`. **The current build script does not automatically apply every release patch**, so its output may differ from the tested v0.1.0 app.
- Graphics packaging, standalone library linking, and the original Chobby archive still need independent build verification.
- Do not replace your installed `/Applications/Zero-K.app` with an untested build.

For exact source revisions and the release's additional manual steps, see [SOURCE-BUILD-NOTES.md](SOURCE-BUILD-NOTES.md). For more technical work still outstanding, see [BUILD-REPRODUCIBILITY-TRACKER.md](BUILD-REPRODUCIBILITY-TRACKER.md).
