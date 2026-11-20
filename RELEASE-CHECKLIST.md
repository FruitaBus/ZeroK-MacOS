# Before making the release public

- [ ] Review Valve Steam API binary provenance and redistribution permissions.
- [ ] Review all third-party licenses and attribution; confirm source obligations.
- [ ] Make the exact corresponding source and build scripts available for all
      covered distributed components, including custom Mesa, AI and game assets.
- [ ] Review the source snapshot for private tokens, account data and secrets.
- [ ] Confirm the Chobby and Recoil patch source can be rebuilt on a clean machine.
- [ ] Test the packaged DMG on a second Apple Silicon Mac (macOS 26+).
- [ ] Check Gatekeeper behavior; ad hoc signatures are not Developer ID signatures.
- [ ] Sign with Developer ID and notarize if distributing for ordinary Mac users;
      rebuilding or re-signing requires retesting and a NEW checksum/DMG.
- [ ] Review experimental Lua inactive-table-key handling for correctness.
- [ ] Verify multiplayer synchronization and long-session stability separately.
- [ ] Publish source alongside any binary offered for download.

Creating a **private GitHub draft** is staging, not permission or proof of compliance.
