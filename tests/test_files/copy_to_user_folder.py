"""
Copy the user instruments to the user folder.
"""

import glob
import os
import shutil

from src.app_data import AppData


def copy_to_user_folder():
    n_copied = 0
    for source in glob.glob("instrument_*.json"):
        destination = os.path.join(AppData.USER_FOLDER, source)
        print(f"Copy: {source} to: {destination}")
        shutil.copy2(source, destination)
        n_copied += 1
    print(f"\n{n_copied} instruments copied")

    n_copied = 0
    for source in glob.glob("configuration_*.json"):
        destination = os.path.join(AppData.USER_FOLDER, source)
        print(f"Copy: {source} to: {destination}")
        shutil.copy2(source, destination)
        n_copied += 1
    print(f"\n{n_copied} configurations copied")


if __name__ == "__main__":

    import pylint

    copy_to_user_folder()
    pylint.run_pylint([__file__])
