# Hints

## Requirements

The following tools are required to build this code-unit:

- `git`
- `python`
- `scriptcollection`
- `docfx`
- `powershell`
- Visual Studio (with the C++-workload) **and the Windows-SDK** for building the native
  Win32-OpenSSH-sources. Without the SDK the build of the upstream stops with
  `Cannot find path 'C:\Program Files (x86)\Windows Kits\10\Lib'`. The buildhelper of the upstream can
  install its dependencies by itself (`Start-OpenSSHBootstrap`), but that installs software on the
  machine and needs elevated privileges, so it is not done by the build of this codeunit.

To create a release the following tools are also required:

- `gh`

This codeunit is buildable on Windows only: the upstream is the Windows-variant of OpenSSH and its
buildhelper is a PowerShell-module which drives MSBuild.

## IDE

The recommended IDE for this codeunit is [Visual Studio Code](https://code.visualstudio.com/).

## Build-output

The build compiles the upstream located at the repository-level folder `Other/Resources/Upstream` and places
the resulting binaries in `Other/Artifacts/BuildResult_Win32OpenSSH_<arch>`. The architectures which are built
and the configuration are stated at the top of `Other/Build/Build.py`.

## Why the build works on a copy of the upstream

The buildhelper of the upstream determines the folder it writes its logs and its intermediate results into by
walking upwards until it finds a folder named `.git` (see `Get-RepositoryRoot` in
`OpenSSHCommonUtils.psm1`). Inside this repository the first hit is the `.git` of SSHM itself, so the upstream
would write outside of its own folder and the build would fail.

`Other/Build/Build.py` therefore copies the upstream into the (git-ignored) artifacts-folder, puts an empty
`.git`-folder beside that copy and builds there. That is also what keeps the build from modifying anything
which is tracked.

## Why this codeunit does not use one of the codeunit-type-specific automations

ScriptCollection has no automation for C, and what is compiled here is a foreign project which is built by its
own buildhelper. The scripts of this codeunit are therefore written directly instead of delegating to such an
automation. What they still use from ScriptCollection is the general part (version, constants, license), so
the codeunit behaves like every other one from the outside.
