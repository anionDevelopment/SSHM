import os
from pathlib import Path
from ScriptCollection.GeneralUtilities import GeneralUtilities
from ScriptCollection.ScriptCollectionCore import ScriptCollectionCore


# Architectures which are built. Each entry must be a value accepted by the upstream
# buildhelper (Start-OpenSSHBuild/-Package): "x64", "x86", "arm64" or "arm".
ARCHITECTURES: list[str] = ["x64"]

# Build-configuration which is passed to the upstream buildhelper ("Release" or "Debug").
CONFIGURATION: str = "Release"


def build():
    # SSHM does not contain own source-code. The source which is compiled is the bundled
    # Win32-OpenSSH-upstream which lives at the repository-level folder "Other/Resources/Upstream"
    # (added as git-subtree). This build invokes the upstream's own PowerShell-buildhelper
    # (Start-OpenSSHBuild/Start-OpenSSHPackage) directly and places the resulting binaries in the
    # mandatory artifacts-folder "Other/Artifacts/BuildResult_Win32OpenSSH_<arch>".
    sc = ScriptCollectionCore()
    current_file = str(Path(__file__).absolute())
    codeunit_folder = GeneralUtilities.resolve_relative_path("../..", os.path.dirname(current_file))
    repository_folder = GeneralUtilities.resolve_relative_path("..", codeunit_folder)
    upstream_folder = GeneralUtilities.resolve_relative_path("Other/Resources/Upstream", repository_folder)
    GeneralUtilities.assert_condition(os.path.isdir(upstream_folder), f"The upstream-folder '{upstream_folder}' does not exist.")
    buildhelper = GeneralUtilities.resolve_relative_path("contrib/win32/openssh/OpenSSHBuildHelper.psm1", upstream_folder)
    GeneralUtilities.assert_condition(os.path.isfile(buildhelper), f"The upstream-buildhelper '{buildhelper}' does not exist.")
    artifacts_folder = os.path.join(codeunit_folder, "Other", "Artifacts")
    for architecture in ARCHITECTURES:
        sc.log.log(f"Build Win32-OpenSSH for architecture '{architecture}' ({CONFIGURATION})...")
        # Only the BuildResult-subfolder of this architecture is (re)created here so that artifacts
        # which were produced by the common-tasks (e.g. the License-artifact) are kept.
        build_result_folder = os.path.join(artifacts_folder, f"BuildResult_Win32OpenSSH_{architecture}")
        GeneralUtilities.ensure_folder_exists_and_is_empty(build_result_folder)
        powershell_command = (
            "$ErrorActionPreference='Stop';"
            f" Import-Module '{buildhelper}' -Force;"
            f" Start-OpenSSHBuild -NativeHostArch {architecture} -Configuration {CONFIGURATION} -Verbose;"
            f" Start-OpenSSHPackage -NativeHostArch {architecture} -Configuration {CONFIGURATION} -DestinationPath '{build_result_folder}' -Verbose"
        )
        sc.run_program_argsasarray(
            "powershell",
            ["-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-Command", powershell_command],
            upstream_folder,
            print_live_output=True)
        GeneralUtilities.assert_condition(
            len(GeneralUtilities.get_direct_files_of_folder(build_result_folder)) > 0,
            f"The build did not produce any binaries in '{build_result_folder}'.")


if __name__ == "__main__":
    build()
