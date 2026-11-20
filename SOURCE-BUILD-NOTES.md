# Source and build guidance — 0.1.0

1. Use the exact pins in `sources.lock.json` and `assets.lock.json`. The Git
   revisions in these files are source provenance, not proof that remote repos
   or downloads are currently accessible. Verify downloaded asset SHA-256 values.
2. For Recoil, check out commit `199b752a79f5c9211d88986c98bef1482ea2f1f9` from the recorded
   fork, and apply `release-patches/recoil-lua-save-fix.patch` with `git apply`.
   Do not blindly copy old `.before-*` development backups.
3. For the Chobby `.sdz` built from revision `7462a1bdf6e93815a556458fff63a85abdcee95e`,
   apply `python3 release-patches/patch-chobby-version.py PATH/TO/Chobby-macos.sdz`.
   This updates the configured default game to Zero-K v1.14.10.3 and disables
   the rapid tag. The configuration was reproduced member-for-member against the
   tested archive. The build of the original archive itself is not reproduced here.
4. The tested `games/zk.sdd/modinfo.lua` is preserved as
   `packaged-game-config/zk-modinfo.lua`. Its name/shortname fields were adjusted
   during packaging; ensure that the source game data used to assemble the app
   matches this file. Other local changes to `zkmenu.sdd` are not captured by
   the Chobby archive patch; that directory should be reviewed before rebuilding.
5. ZkMacOS launcher and packaging sources are under `port-source/`. See
   `port-source/README.md` and `port-source/scripts/build-app.sh` for the original
   workflow; review before using. Compiling `spring` again restores development
   Homebrew install names, so standalone dependency relinking is required before
   installing the new engine in any signed app. Ad hoc signing is not notarization.
6. The distributable also contains Mesa/Zink/KosmicKrisp and bundled native
   libraries. Review and supply the corresponding source/patches, precise build
   configurations, licenses, and installation materials as applicable.

The external Recoil/Chobby/Infrastructure repositories are **not vendored** in
this lightweight GitHub source snapshot. For a complete GPL corresponding-source
delivery, ensure the exact upstream source trees and required build dependencies
are reliably obtainable by recipients, and provide any additional changes and
scripts needed to rebuild the distributed components. External URLs/patches alone
may not resolve all source-distribution obligations.
