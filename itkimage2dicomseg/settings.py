"""
    @file:              settings.py
    @Author:            Maxence Larose

    @Creation Date:     01/2022
    @Last modification: 01/2022

    @Description:       Stores custom enumerations of the important file names, folder names and paths within the
                        project.
"""

from os.path import abspath, dirname, join

ROOT = abspath(dirname(__file__))


class FileName:
    METADATA_JSON: str = "metadata.json"


class FolderName:
    DATA_FOLDER: str = "data"
    PATIENTS_FOLDER: str = "Patients"
    SEGMENTATIONS_FOLDER: str = "Segmentations"
    PATIENT_IMAGES_FOLDER: str = "images"
    PATIENT_SEGMENTATIONS_FOLDER: str = "segmentations"


class PathName:
    PATH_TO_DATA_FOLDER: str = join(ROOT, FolderName.DATA_FOLDER)

    PATH_TO_METADATA_JSON: str = join(PATH_TO_DATA_FOLDER, FileName.METADATA_JSON)
    PATH_TO_PATIENTS_FOLDER: str = join(PATH_TO_DATA_FOLDER, FolderName.PATIENTS_FOLDER)
    PATH_TO_SEGMENTATIONS_FOLDER: str = join(PATH_TO_DATA_FOLDER, FolderName.SEGMENTATIONS_FOLDER)
