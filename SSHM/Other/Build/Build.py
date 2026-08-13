import os
import shutil
from pathlib import Path
from ScriptCollection.GeneralUtilities import GeneralUtilities
from ScriptCollection.ScriptCollectionCore import ScriptCollectionCore

# Architectures which are built. Each entry must be a value accepted by the upstream buildhelper
# (Start-OpenSSHBuild/-Package): "x64", "x86", "arm64" or "arm".
_Architectures: list[str] = ["x64"]

# Build-configuration which is passed to the upstream buildhelper ("Release" or "Debug").
_Configuration: str = "Release"

# The folder the sourcecode of the upstream is bundled in (relative to the repository-folder).
_UpstreamFolder: str = "Other/Resources/Upstream"


def build():
    """Compiles the bundled Win32-OpenSSH-upstream and provides its binaries as artifact.

    SSHM has no own sourcecode: what is compiled is the bundled upstream, and it is compiled by the
    buildhelper of that upstream (a PowerShell-module), because reimplementing its build here would mean to
    maintain a second build for a foreign project."""
    sc = ScriptCollectionCore()
    codeunit_folder = GeneralUtilities.resolve_relative_path("../..", os.path.dirname(str(Path(__file__).absolute())))
    repository_folder = GeneralUtilities.resolve_relative_path("..", codeunit_folder)
    upstream_folder = GeneralUtilities.resolve_relative_path(_UpstreamFolder, repository_folder)
    GeneralUtilities.assert_condition(os.path.isdir(upstream_folder), f"The upstream-folder \"{upstream_folder}\" does not exist.")
    artifacts_folder = os.path.join(codeunit_folder, "Other", "Artifacts")
    build_folder = os.path.join(artifacts_folder, "Build")

    for architecture in _Architectures:
        sc.log.log(f"Build Win32-OpenSSH for architecture \"{architecture}\" ({_Configuration})...")
        upstream_copy = prepare_upstream_copy(upstream_folder, build_folder)
        buildhelper = os.path.join(upstream_copy, "contrib", "win32", "openssh", "OpenSSHBuildHelper.psm1")
        GeneralUtilities.assert_condition(os.path.isfile(buildhelper), f"The upstream-buildhelper \"{buildhelper}\" does not exist.")
        # Only the BuildResult-subfolder of this architecture is (re)created here, so that artifacts which were
        # produced by the common-tasks (for example the license-artifact) are kept.
        build_result_folder = os.path.join(artifacts_folder, f"BuildResult_Win32OpenSSH_{architecture}")
        GeneralUtilities.ensure_folder_exists_and_is_empty(build_result_folder)
        powershell_command = (
            "$ErrorActionPreference='Stop';"
            f" Import-Module '{buildhelper}' -Force;"
            f" Start-OpenSSHBuild -NativeHostArch {architecture} -Configuration {_Configuration} -Verbose;"
            f" Start-OpenSSHPackage -NativeHostArch {architecture} -Configuration {_Configuration} -DestinationPath '{build_result_folder}' -Verbose"
        )
        sc.run_program_argsasarray(
            "powershell",
            ["-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-Command", powershell_command],
            upstream_copy,
            print_live_output=True)
        GeneralUtilities.assert_condition(
            0 < len(GeneralUtilities.get_direct_files_of_folder(build_result_folder)),
            f"The build did not produce any binaries in \"{build_result_folder}\".")


def prepare_upstream_copy(upstream_folder: str, build_folder: str) -> str:
    """Copies the upstream into the artifacts-folder and marks that copy as the root of a repository.

    Two reasons for the copy: the build writes its logs and its intermediate results beside the sourcecode, and
    the upstream determines the folder it writes them into by walking upwards until it finds a folder named
    ".git" (see Get-RepositoryRoot of OpenSSHCommonUtils.psm1). Inside this repository the first hit is the
    ".git" of SSHM itself, so the upstream would write outside of its own folder and the build would fail. The
    copy gets an empty ".git"-folder, which is what makes the upstream treat the copy as its root; and because
    the copy lies in the (git-ignored) artifacts-folder, the build does not modify anything which is tracked."""
    upstream_copy = os.path.join(build_folder, "Upstream")
    GeneralUtilities.ensure_directory_does_not_exist(upstream_copy)
    GeneralUtilities.ensure_directory_exists(upstream_copy)
    shutil.copytree(upstream_folder, upstream_copy, dirs_exist_ok=True)
    GeneralUtilities.ensure_directory_exists(os.path.join(upstream_copy, ".git"))
    return upstream_copy


if __name__ == "__main__":
    build()
