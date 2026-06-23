import os
from pathlib import Path
from ScriptCollection.GeneralUtilities import GeneralUtilities
from ScriptCollection.ScriptCollectionCore import ScriptCollectionCore


def generate_reference():
    sc = ScriptCollectionCore()
    reference_folder = os.path.dirname(str(Path(__file__).absolute()))
    generated_reference_folder = GeneralUtilities.resolve_relative_path("../Artifacts/Reference", reference_folder)
    GeneralUtilities.ensure_directory_does_not_exist(generated_reference_folder)
    GeneralUtilities.ensure_directory_exists(generated_reference_folder)
    obj_folder = os.path.join(reference_folder, "obj")
    GeneralUtilities.ensure_folder_exists_and_is_empty(obj_folder)
    sc.run_program("docfx", "-t default,templates/darkfx docfx.json", reference_folder)
    GeneralUtilities.ensure_directory_does_not_exist(obj_folder)


if __name__ == "__main__":
    generate_reference()
