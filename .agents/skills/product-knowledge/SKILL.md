---
name: product-knowledge
description: What SSHM is, how this repository is structured and which mechanisms exist for building and testing it. Use this before fixing a defect or developing a feature in this repository, to know where things belong and how to verify a change.
---

# SSHM

SSHM is a fork of [OpenSSH for Windows](https://github.com/PowerShell/openssh-portable) with one deliberate
difference: the permission-checks which SSH applies to key-files are removed.

The reason is written out in the `ReadMe.md` of the repository and it is the identity of this product, so it
has to survive every update of the upstream: checking the permissions of a key at the moment it is used does
not protect the key (whoever could copy it has copied it long ago), it only refuses the connection of somebody
who takes care of their keys themselves - which on Windows, with its different permission-model, happens
constantly. Whoever wants SSH to do that check anyway uses SSH and not SSHM.

## Structure of the repository

The repository follows the "common project structure": all sourcecode lives in code-units, and every code-unit
has its own `Other`-folder with its build-, quality-check- and reference-files. Use the
`work-with-common-project-structure`-skill when you need the details of that structure.

There is one code-unit, `SSHM`. It is the first C-code-unit of these repositories, and it has no own
sourcecode: what is compiled is the bundled upstream at the repository-level folder
`Other/Resources/Upstream`.

## Why the scripts are written directly

ScriptCollection has no automation for C, and the upstream is built by its own PowerShell-buildhelper
(`Start-OpenSSHBuild` / `Start-OpenSSHPackage`). Reimplementing that build here would mean maintaining a
second build for a foreign project, so `Other/Build/Build.py` calls the buildhelper of the upstream. What the
scripts still use from ScriptCollection is the general part (version, constants, license), so the code-unit
behaves like every other one from the outside.

The linting only normalizes the own scripts. The C-sourcecode is the unmodified upstream: linting it would
report findings of a foreign project which must not be changed here.

## Two things which are easy to get wrong

- **The build runs on a copy.** The buildhelper of the upstream determines where it writes its logs and its
  intermediate results by walking upwards until it finds a folder named `.git` (`Get-RepositoryRoot` in
  `OpenSSHCommonUtils.psm1`). Inside this repository the first hit is the `.git` of SSHM itself, so the
  upstream would write outside of its own folder. `Build.py` therefore copies the upstream into the
  (git-ignored) artifacts-folder, puts an empty `.git`-folder beside that copy and builds there.
- **The build needs the Windows-SDK.** Without it the upstream stops with
  `Cannot find path 'C:\Program Files (x86)\Windows Kits\10\Lib'`. The buildhelper could install its
  dependencies by itself (`Start-OpenSSHBootstrap`), but that installs software and needs elevated
  privileges, so the build of this code-unit does not do it. This code-unit is buildable on Windows only.

## Updating the upstream

The upstream is bundled (not a submodule), so an update means bringing the new state into
`Other/Resources/Upstream` and re-applying the removal of the permission-checks. After such an update, check
that those checks are really gone again - that is the whole point of this fork.
