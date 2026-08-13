import os
from pathlib import Path
from ScriptCollection.GeneralUtilities import GeneralUtilities
from ScriptCollection.ScriptCollectionCore import ScriptCollectionCore


def linting():
    """Checks what belongs to this codeunit.

    The C-sourcecode which is compiled is the unmodified upstream (see Build.py). Linting it would only report
    findings of a foreign project which must not be changed here, so what is checked is what this repository
    really owns: its own scripts. They are normalized (line-endings and invisible characters), which is what
    keeps the repository free of differences which are caused by the machine somebody worked on."""
    sc = ScriptCollectionCore()
    codeunit_folder = GeneralUtilities.resolve_relative_path("../..", os.path.dirname(str(Path(__file__).absolute())))
    sc.normalize_invisible_characters_of_files_in_folder(os.path.join(codeunit_folder, "Other"), ["py", "md", "xml"])


if __name__ == "__main__":
    linting()
