# Vendored Binary

- Project: `DeusData/codebase-memory-mcp`
- Source: <https://github.com/DeusData/codebase-memory-mcp>
- Version: `0.9.0`
- Platform: `darwin-arm64`
- File: `scripts/vendor/codebase-memory-mcp-darwin-arm64`
- SHA-256: `dc7a383664b5fda407f22a81df538c6282c5dbbcc58cf3c97605dbd5dcf13d79`
- Vendored: `2026-07-11`
- License: MIT; see `scripts/vendor/LICENSE.codebase-memory-mcp`

The binary is an ad-hoc-signed, thin arm64 Mach-O copied from the locally installed upstream release. It links only to macOS system libraries (`libSystem`, `libc++`, and `libz`). The `scripts/cbm` wrapper prevents server mode and agent configuration commands.

To update it, obtain an official macOS arm64 release, verify the published checksum, replace the binary, update this record, confirm its ad-hoc signature, and rerun the skill validation and CLI fixture tests.
