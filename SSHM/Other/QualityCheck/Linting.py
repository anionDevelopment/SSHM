from ScriptCollection.TFCPS.CPP.TFCPS_CodeUnitSpecific_CPP import TFCPS_CodeUnitSpecific_CPP_Functions, TFCPS_CodeUnitSpecific_CPP_CLI


def linting():
    """Checks what belongs to this codeunit.

    The C-sourcecode which is compiled is the unmodified upstream (see Build.py). Linting it would only report
    findings of a foreign project which must not be changed here, so the generic linting of TFCPS_CodeUnitSpecific_CPP
    (which only normalizes this repository's own scripts) is used as-is."""
    tf: TFCPS_CodeUnitSpecific_CPP_Functions = TFCPS_CodeUnitSpecific_CPP_CLI.parse(__file__)
    tf.linting()


if __name__ == "__main__":
    linting()
