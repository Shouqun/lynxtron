---
'@lynx-js/cef-webview': patch
'@lynx-js/lynxtron-builder': patch
'@lynx-js/lynxtron': patch
'create-lynxtron': patch
---

Build CEF webview for an explicit target architecture using one macOS build
entry point for local development and CI. Prepare target-specific CEF artifacts
without requiring the build host's Node executable to run under Rosetta.

Allow source builds to skip runtime downloads before publication and package
AutoLink libraries once, from `.lynxtron/native`, without duplicate application
resources or regular `node_modules` payloads.
