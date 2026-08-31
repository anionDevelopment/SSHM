import os
import shutil
from ScriptCollection.GeneralUtilities import GeneralUtilities
from ScriptCollection.TFCPS.CPP.TFCPS_CodeUnitSpecific_CPP import TFCPS_CodeUnitSpecific_CPP_Functions, TFCPS_CodeUnitSpecific_CPP_CLI

# The folder the sourcecode of the upstream is bundled in (relative to the repository-folder, kept in sync via
# "git subtree", see the ReadMe). This is specific to this repository (a fork which vendors a foreign upstream)
# and therefore not part of the generic C/C++-codeunit-support in ScriptCollection.
_UpstreamFolder: str = "Other/Resources/Upstream"


def common_tasks():
    tf: TFCPS_CodeUnitSpecific_CPP_Functions = TFCPS_CodeUnitSpecific_CPP_CLI.parse(__file__)
    tf.do_common_tasks(tf.get_version_of_project())  # codeunit-version should always be the same as project-version
    copy_upstream_to_src(tf)


def copy_upstream_to_src(tf: TFCPS_CodeUnitSpecific_CPP_Functions) -> None:
    """Copies the bundled Win32-OpenSSH-upstream into the sourcecode-folder of this codeunit.

    SSHM has no sourcecode of its own: what is compiled is the bundled upstream. The sourcecode-folder is
    therefore not maintained by hand: it is replaced completely on every run so that it can never diverge from
    the bundled upstream (Other/Resources/Upstream)."""
    upstream_folder = GeneralUtilities.resolve_relative_path(_UpstreamFolder, tf.get_repository_folder())
    GeneralUtilities.assert_condition(os.path.isdir(upstream_folder), f"The upstream-folder \"{upstream_folder}\" does not exist.")
    src_folder = os.path.join(tf.get_codeunit_folder(), "src")
    GeneralUtilities.write_message_to_stdout(f"Copy upstream-sourcecode to \"{src_folder}\"...")
    GeneralUtilities.ensure_directory_does_not_exist(src_folder)
    GeneralUtilities.ensure_directory_exists(src_folder)
    shutil.copytree(upstream_folder, src_folder, dirs_exist_ok=True)


if __name__ == "__main__":
    common_tasks()
