"""
    @file:              data_destructure_preprocessing.py
    @Author:            Maxence Larose

    @Creation Date:     01/2022
    @Last modification: 01/2022

    @Description:       Rearrange the data folder structure so that a patient folder contains all of his DICOM files,
                        including the newly created DICOM SEG files.
"""
import logging

from .patients_folder_structure.destructure import destructure_patients_folder
from .logging_tools import logs_file_setup
from .settings import *

if __name__ == "__main__":
    # ----------------------------------------------------------------------------------------------------------- #
    #                                          Logs Setup                                                         #
    # ----------------------------------------------------------------------------------------------------------- #
    logs_file_setup(logging.INFO)

    # ----------------------------------------------------------------------------------------------------------- #
    #                                           Destructure folder                                                #
    # ----------------------------------------------------------------------------------------------------------- #
    destructure_patients_folder(
        path_to_patients_folder=PathName.PATH_TO_PATIENTS_FOLDER,
        patient_images_folder_name=FolderName.PATIENT_IMAGES_FOLDER,
        patient_segmentations_folder_name=FolderName.PATIENT_SEGMENTATIONS_FOLDER
    )
