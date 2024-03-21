"""
Copy the user instruments to the user folder.
"""

import glob
import os
import shutil

from src.app_data import AppData


_IGNORE_FILES = [
    os.path.join(AppData.USER_FOLDER, "LilyDataLoggerStudioCE.json"),
    os.path.join(AppData.USER_FOLDER, "LilyDataLoggerStudioCE.log")
]


def _clean_user_folder():
    matches = list(filter(lambda x: x not in _IGNORE_FILES,
                          glob.glob(os.path.join(AppData.USER_FOLDER, "*.*"))))
    for item in matches:
        print(f"Delete {item}")
        os.unlink(item)


def _copy_items(file_filter):
    n_copied = 0
    for source in glob.glob(file_filter):
        destination = os.path.join(AppData.USER_FOLDER, source)
        print(f"Copy: {source} to: {destination}")
        shutil.copy(str(source), str(destination))
        n_copied += 1
    return n_copied


def copy_to_user_folder():
    _clean_user_folder()
    n_copied = _copy_items("instrument_*.json")
    print(f"\n{n_copied} files copied")


if __name__ == "__main__":

    copy_to_user_folder()
