from ScriptCollection.TFCPS.CPP.TFCPS_CodeUnitSpecific_CPP import TFCPS_CodeUnitSpecific_CPP_Functions, TFCPS_CodeUnitSpecific_CPP_CLI


def build():
    """Compiles the sourcecode of this codeunit and provides the resulting binaries as artifact.

    SSHM has no sourcecode of its own: the sourcecode-folder (src) is a copy of the bundled Win32-OpenSSH
    upstream, placed there by CommonTasks.py. Only the windows-target is built here: SSHM is a Windows-port of
    OpenSSH, so this is the only target-platform "task bb" needs. The generic C/C++-codeunit-support
    (TFCPS_CodeUnitSpecific_CPP) also supports a linux- and a macos-target for a codeunit which needs them."""
    tf: TFCPS_CodeUnitSpecific_CPP_Functions = TFCPS_CodeUnitSpecific_CPP_CLI.parse(__file__)
    # Architectures which are built. Each entry must be a value MSBuild accepts as "/p:Platform": "x64", "x86",
    # "arm64" or "arm".
    tf.architectures = ["x64"]
    tf.configuration = "Release"
    tf.windows_solution_file = "contrib/win32/openssh/Win32-OpenSSH.sln"
    tf.build(["windows"])


if __name__ == "__main__":
    build()
