# @lynx-js/cef-webview

A `<webview>` element implementation based on Chromium Embedded Framework (CEF) for Lynxtron.

## Overview

This library provides a CEF-based implementation of the `<webview>` element for Lynxtron applications. It allows you to embed Chromium-based web content within your Lynxtron app, providing a full-featured web browsing experience.

## Installation

```bash
npm install @lynx-js/cef-webview
```

## Usage

Enable the Lynxtron autolink plugin in your application build. AutoLink requires
`@lynx-js/cef-webview/lynxtron`, which loads the current platform's Lynxtron
addon so its static Lynx registrations run during startup. CEF itself is
initialized only when you call `initialize()`.

The package selects its native addon from `lynx.lib.json`. On Windows, it also
ships the CEF DLLs, resource packs, and locales next to that addon and adds the
selected runtime directory to the DLL search path before loading it.
On macOS, AutoLink embeds the CEF Framework and the package-owned
`LynxtronWebview Helper` app bundles into the host application.

```ts
import cefWebview from '@lynx-js/cef-webview/lynxtron';

cefWebview.initialize();
```

Once initialized, you can use the `<webview>` element in your Lynx templates:

```xml
<webview src="https://www.example.com" width="100%" height="500px"></webview>
```

## Building

### Prerequisites

- macOS with Xcode Command Line Tools, Python 3, Git, and network access.

### Build Steps

From the repository root, use the same entry point as the release workflow:

```bash
python3 lynxtron_tools/build_cef_webview.py --arch x64
```

Use `--arch arm64` for Apple Silicon output. The script prepares host-native
Node and CMake, the pinned Lynx source and headers, and the target CEF SDK via
the shared build environment setup and Habitat. The separate
`prepare_mac_cross_compile_env.py` configures the target before dependency sync;
the build entry calls the package's normal `build` command and checks the
architecture of the addon, framework, and helper executables. An M1 host can
produce x64 output without running Node under Rosetta. Use a clean checkout:
the shared preparation synchronizes dependencies and applies repository patches.

Add `--version <version>` to create the release zip in `publish/`.

When building CEF against a Windows runtime built from source, set
`LYNXTRON_IMPORT_LIB` to the absolute path of that build's
`out/Release/lynxtron.dll.lib` before invoking the package's `build` command.
The build validates the file and forwards it to CMake; an invalid override
fails instead of falling back to an installed runtime. Without an override,
the existing npm runtime import-library resolution remains in effect.

For Windows source builds, after building the Lynxtron runtime, invoke the same
entry point used by CI and publishing from PowerShell:

```powershell
.\lynxtron_tools\build_cef_webview.ps1 -Arch x64
```

It configures the build environment, syncs the CEF SDK, passes the source-built
import library, calls the package build, and checks the addon, subprocess and
CEF DLL. Environment variables and the working directory are restored on exit.

## Dependencies

- **Runtime Dependencies:**

  - js-yaml
  - plist

- **Development Dependencies:**
  - node-addon-api
  - cmake-js
  - lynxtron

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Authors

Lynxtron Authors
