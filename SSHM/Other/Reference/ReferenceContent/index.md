# SSHM reference

SSHM compiles the bundled Win32-OpenSSH-upstream. `CommonTasks.py` copies it from the repository-level folder
`Other/Resources/Upstream` into the sourcecode-folder (`src`) of this codeunit, and `Build.py` compiles that
sourcecode-folder, providing the resulting OpenSSH-for-Windows binaries as build-artifact
(`Other/Artifacts/BuildResult_Windows_<arch>`).

This codeunit does not contain own source-code; see the upstream-repository for the documentation of the produced tools (`ssh`, `sshd`, `scp`, `sftp`, `ssh-keygen`, ...).
