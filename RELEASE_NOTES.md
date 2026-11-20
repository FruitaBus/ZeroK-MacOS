# Zero-K 0.1.0 for Apple Silicon — test preview

Unofficial, experimental macOS port. Not affiliated with the official Zero-K team.

- ARM64 standalone app for macOS 26.0 or later
- Includes Zero-K v1.14.10.3, bundled Chobby menu and selected maps
- Tested AI skirmishes and save/load cycles on an M4 Pro Mac
- DMG installed and started a match outside the development directory

**Known limitations:** This DMG is ad-hoc signed, not notarized. Multiplayer,
other Macs and long sessions are not yet fully validated. The Lua serialization
correction remains experimental. The package includes third-party components,
including a Steam API binary; confirm redistribution terms before public release.

Binary SHA-256: `b7e5cc0282b996916a732d58108686975d75a22bbb8af9a3348fc962f49481fb`
Source and notices: this GitHub repository. See `RELEASE-CHECKLIST.md`.
