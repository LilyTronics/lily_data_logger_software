"""
Script that runs before all tests to set up the environment
"""

import os
import shutil


def clear_reports(report_path):
    print("Clear report path: {}".format(report_path))
    for item in os.listdir(report_path):
        full_path = os.path.join(report_path, item)
        if os.path.isfile(full_path):
            os.remove(full_path)
        elif os.path.isdir(full_path):
            shutil.rmtree(full_path)
        else:
            raise Exception("ERROR: could not remove item '{}'".format(item))


if __name__ == "__main__":

    clear_reports("..\\test_reports")
