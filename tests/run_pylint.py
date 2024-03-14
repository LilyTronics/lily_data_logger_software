"""
Run pylint

Use this as a guideline to check if code is more or less consistent.
It is not used to solve every issue, because pylint is also not perfect.
"""

import os
import pylint

arguments = [
    # The wx library is not properly handled
    "--ignored-modules=wx",
    # Cyclic imports are not properly handled
    "--disable=cyclic-import",
    # We do not want doc strings everywhere, we believe in self-explanatory code
    "--disable=missing-class-docstring",
    "--disable=missing-function-docstring",
    # We determine ourselves how we handle exceptions, thank you very much
    "--disable=broad-exception-caught",
    "--disable=broad-exception-raised",
    # Not relevant how many public methods there are
    "--disable=too-few-public-methods",
    # We want to use as many as needed,
    # except for too-many-statements and too-many-nested-blocks
    "--disable=too-many-instance-attributes",
    "--disable=too-many-arguments",
    "--disable=too-many-locals",
    # We have our own preferred import order
    "--disable=wrong-import-order"
]

for current_folder, sub_folders, filenames in os.walk(".."):
    sub_folders.sort()
    # Skip files in local environment
    if current_folder.startswith(os.path.join("..", ".venv")):
        continue
    # Skip files in build output
    if current_folder.startswith(os.path.join("..", "deployment", "build_output")):
        continue
    # Skip files used for documentation
    if current_folder.startswith(os.path.join("..", "docs")):
        continue
    for filename in filter(lambda x: x.endswith(".py"), filenames):
        filepath = os.path.join(current_folder, filename)
        print(f"Adding: {filepath}")
        arguments.append(filepath)


pylint.run_pylint(arguments)
