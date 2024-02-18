"""
Creates a deployment package.
"""

import os
import shutil
import zipfile
import PyInstaller.__main__
import src

from src.app_data import AppData


def _clean_output_folder(output_folder):
    print("Clean output folder . . .")
    if os.path.isdir(output_folder):
        for item in os.listdir(output_folder):
            full_path = os.path.join(output_folder, item)
            if os.path.isfile(full_path):
                os.remove(full_path)
            elif os.path.isdir(full_path):
                shutil.rmtree(full_path)
    else:
        os.makedirs(output_folder)


def _create_version_file(version_file, artifacts_path):
    print("Create version file . . .")
    version_template = os.path.join(artifacts_path, "version.template")
    version_tuple = list(map(int, AppData.VERSION.split('.')))
    while len(version_tuple) < 4:
        version_tuple.append(0)
    with open(version_template, "r", encoding="utf-8") as fp:
        version_template = fp.read()
        version_template = version_template.replace("{app_name}", AppData.APP_NAME)
        version_template = version_template.replace("{version_tuple}", str(version_tuple))
        version_template = version_template.replace("{version_string}", AppData.VERSION)
        version_template = version_template.replace("{exe_name}", AppData.EXE_NAME)
        version_template = version_template.replace("{company_name}", AppData.COMPANY)

    with open(version_file, "w", encoding="utf-8") as fp:
        fp.write(version_template)


def _create_zip_file(dist_path, artifacts_path):
    print("Create ZIP file for distribution . . .")
    zip_filename = os.path.join(dist_path, f"{AppData.EXE_NAME}_{AppData.VERSION}.zip")
    with zipfile.ZipFile(zip_filename, "w") as zip_object:
        # Add dist files
        app_path = os.path.join(dist_path, AppData.EXE_NAME)
        for current_folder, sub_folders, filenames in os.walk(str(app_path)):
            sub_folders.sort()
            for filename in filenames:
                full_path = os.path.join(current_folder, filename)
                target_name = full_path[len(app_path) + 1:]
                print(f"Add: {full_path} to zip as: {target_name}")
                zip_object.write(full_path, target_name)
        # Add arduino DAQ sketch
        sketch_path = os.path.join(artifacts_path, "lily_arduino_daq", "lily_arduino_daq.ino")
        target_name = os.path.join("lily_arduino_daq", "lily_arduino_daq.ino")
        print(f"Add: {sketch_path} to zip as: {target_name}")
        zip_object.write(sketch_path, target_name)


def create_deployment():
    artifacts_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "artifacts"))
    init_file = os.path.join(os.path.dirname(src.__file__), "main.pyw")
    icon_file = os.path.join(artifacts_path, "app.ico")
    output_folder = os.path.join(os.path.dirname(__file__), 'build_output')
    dist_path = os.path.join(output_folder, "dist")
    version_file = os.path.join(output_folder, "app.version")

    print(f"\n{("=" * 120)}")
    print("Build settings:")
    print("Init file       :", init_file)
    print("Application icon:", icon_file)
    print("Artifacts folder:", artifacts_path)
    print("Output folder   :", output_folder)
    print("Dist folder     :", dist_path)
    print("Version file    :", version_file)
    print(f"{("=" * 120)}\n")

    _clean_output_folder(output_folder)
    _create_version_file(version_file, artifacts_path)

    PyInstaller.__main__.run([
        init_file,
        "--clean",
        "--onedir",
        "--noconsole",
        f"--name={AppData.EXE_NAME}",
        f"--icon={icon_file}",
        f"--version-file={version_file}",
        "--contents=lib",
        f"--workpath={os.path.join(output_folder, "work")}",
        f"--specpath={os.path.join(output_folder, "spec")}",
        f"--distpath={dist_path}"
    ])

    _create_zip_file(dist_path, artifacts_path)

    print("\nBuild done")


if __name__ == "__main__":

    import pylint

    create_deployment()
    pylint.run_pylint([__file__])
