# Hints

## Requirements

The following tools are required to build this code-unit:

- `git`
- `gitversion`
- `python`
- `scriptcollection`
- `docfx`
- `powershell`
- Visual Studio (with the C++-workload and the Windows-SDK) for building the native Win32-OpenSSH-sources

To create a release the following tools are also required:

- `gh`

## IDE

The recommended IDE for this codeunit is [Visual Studio Code](https://code.visualstudio.com/).

## Build-output

The build compiles the upstream located at the repository-level folder `Other/Resources/Upstream` and places the resulting binaries in `Other/Artifacts/BuildResult_Win32OpenSSH_<arch>`. The built architecture(s) and the configuration can be adjusted via `SSHM_ARCHITECTURES` and `SSHM_CONFIGURATION` in `Other/SSHMCodeUnit.py`.
