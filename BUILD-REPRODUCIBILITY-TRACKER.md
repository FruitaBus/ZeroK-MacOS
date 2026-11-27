# Build reproducibility acceptance tracker

These are open engineering tasks, **not completed claims**.

- [ ] Ensure top-level `sources.lock.json` and `assets.lock.json` are accessible to `port-source` fetch scripts, without creating duplicate diverging lockfiles.
- [ ] Fetch pinned Recoil/Chobby/Infrastructure repositories and verify exact Git SHAs.
- [ ] Integrate `recoil-lua-save-fix.patch` with a strict zero-fuzz application check, tracking whether the fork already includes it.
- [ ] Reconcile the full source for custom engine, launcher, Mesa, KosmicKrisp and all bundled native dependencies.
- [ ] Reconstruct Chobby archive at the recorded pin and apply *both* configuration and save-name patches to the correct `.sdz`.
- [ ] Audit whether `packaged-game-config/zk-modinfo.lua` matches the game archive actually bundled.
- [ ] Remove developer-specific hardcoded paths and allow per-host toolchain detection.
- [ ] Document and script standalone dylib relinking, `@rpath`, code signing and package layout.
- [ ] Add generated-app tests for `arm64`, `codesign --verify`, `otool -L`, archive presence, content/version metadata, and native runtime dependencies.
- [ ] Build on a second clean Apple Silicon Mac from an empty checkout and document every command.
- [ ] Install the resulting DMG and test skirmish start, save/load, AI, graphics and menus.
- [ ] Review license notices and ensure recipients can obtain complete corresponding source and scripts for redistributed components.
- [ ] Keep published v0.1.0 separate from experimental v0.1.1 fixes.
