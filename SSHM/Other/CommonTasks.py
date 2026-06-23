import os
from pathlib import Path
from ScriptCollection.GeneralUtilities import GeneralUtilities
from ScriptCollection.ScriptCollectionCore import ScriptCollectionCore
from ScriptCollection.TFCPS.TFCPS_Tools_General import TFCPS_Tools_General


def common_tasks():
    sc = ScriptCollectionCore()
    tools = TFCPS_Tools_General(sc)
    current_file = str(Path(__file__).absolute())
    codeunit_folder = GeneralUtilities.resolve_relative_path("..", os.path.dirname(current_file))
    repository_folder = GeneralUtilities.resolve_relative_path("..", codeunit_folder)
    codeunit_file = os.path.join(codeunit_folder, f"{os.path.basename(codeunit_folder)}.codeunit.xml")
    codeunit_version = sc.get_semver_version_from_gitversion(repository_folder)  # codeunit-version should always be the same as project-version
    tools.write_version_to_codeunit_file(codeunit_file, codeunit_version)
    tools.set_default_constants(codeunit_folder)
    tools.copy_licence_file(codeunit_folder)


if __name__ == "__main__":
    common_tasks()
