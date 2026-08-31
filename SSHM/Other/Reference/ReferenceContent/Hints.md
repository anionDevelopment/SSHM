# Hints

## Requirements

The following tools are required to build this code-unit:

- `git`
- `python`
- `scriptcollection`
- `docfx`
- `powershell`
- Visual Studio (with the "Desktop development with C++"-workload, including the Spectre-mitigated
  libraries for the used toolset) **and a Windows-SDK** for building the native Win32-OpenSSH-sources.
  `Build.py` detects and uses whichever Windows-SDK-version is actually installed (see "Why the build
  overrides the Windows-SDK-version" below); the Spectre-mitigated libraries have to be installed by hand
  (Visual Studio Installer, "Individual components", search for "Spectre") because installing them needs
  elevated privileges, which the build of this codeunit does not have (and must not silently request).

To create a release the following tools are also required:

- `gh`

This codeunit is buildable on Windows only: the upstream is the Windows-variant of OpenSSH and its
buildhelper is a PowerShell-module which drives MSBuild.

## IDE

The recommended IDE for this codeunit is [Visual Studio Code](https://code.visualstudio.com/).

## Build-output

`Other/CommonTasks.py` copies the upstream located at the repository-level folder `Other/Resources/Upstream`
into the (git-ignored) sourcecode-folder of this codeunit (`src`), and `Other/Build/Build.py` compiles that
folder with MSBuild, placing the resulting binaries in `Other/Artifacts/BuildResult_Windows_<arch>`. The
architectures and the configuration which are built are stated at the top of `Other/Build/Build.py`.

## Why the sourcecode is a copy of the upstream

SSHM has no sourcecode of its own: what is compiled is the bundled upstream, which is kept in sync with
Win32-OpenSSH via `git subtree` (see the repository-`ReadMe.md`). The sourcecode-folder of this codeunit is
therefore not maintained by hand: `CommonTasks.py` replaces it completely on every run so that it can never
diverge from the bundled upstream.

## Why the build overrides the Windows-SDK-version

The vendored Visual-Studio-solution pins a fixed `WindowsTargetPlatformVersion` (via `paths.targets`), which
only builds if that exact Windows-SDK-version happens to be installed. `Build.py` instead detects whichever
Windows-SDK-version is actually installed on the building machine and passes it to MSBuild as a global
property (`/p:WindowsTargetPlatformVersion=...`), which a project can not override. This avoids depending on
one specific, possibly outdated Windows-SDK-version without having to patch the vendored project.

## Why this codeunit uses TFCPS_CodeUnitSpecific_CPP instead of one of the other codeunit-type-specific automations

Unlike the other codeunit-kinds (`cargo` for Rust, `flutter` for Dart, ...) there is no single, universal
C/C++-build-tool, and what is compiled here is a foreign project (Win32-OpenSSH) with its own build-system.
`TFCPS_CodeUnitSpecific_CPP` in ScriptCollection therefore does not run one fixed command: it standardizes the
plumbing around a native build (locating the sourcecode, verifying and publishing the result, the
reproducible-via-docker option for a linux-target) while the actual build-command per target-platform is
configured by this codeunit (see `Other/Build/Build.py`). Everything specific to this repository being a fork
with a bundled upstream (for example where that upstream lives) stays local to this codeunit instead of living
in ScriptCollection.
