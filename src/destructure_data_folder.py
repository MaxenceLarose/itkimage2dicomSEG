"""
    @file:              data_destructure_preprocessing.py
    @Author:            Maxence Larose

    @Creation Date:     01/2022
    @Last modification: 01/2022

    @Description:       Rearrange the data folder structure so that a patient folder contains all of his DICOM files,
                        including the newly created DICOM SEG files.
"""
import logging

from logging_tools import logs_file_setup
from settings import *
from utils import destructure_data_folder

if __name__ == "__main__":
    # ----------------------------------------------------------------------------------------------------------- #
    #                                          Logs Setup                                                         #
    # ----------------------------------------------------------------------------------------------------------- #
    logs_file_setup(logging.INFO)

    # ----------------------------------------------------------------------------------------------------------- #
    #                                           Destructure folder                                                #
    # ----------------------------------------------------------------------------------------------------------- #
    destructure_data_folder(
        path_to_patients_folder=PathName.PATH_TO_PATIENTS_FOLDER,
        patient_images_folder_name=FolderName.PATIENT_IMAGES_FOLDER,
        patient_segmentations_folder_name=FolderName.PATIENT_SEGMENTATIONS_FOLDER
    )
