---
'@lynx-js/cef-webview': patch
---

Forward an explicit source-build Lynxtron import library to CMake, and use the current Windows runtime build in CI and release jobs instead of relying on downloaded npm artifacts.
