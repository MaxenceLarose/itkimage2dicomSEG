"""
    @file:              data_structure_preprocessing.py
    @Author:            Maxence Larose

    @Creation Date:     01/2022
    @Last modification: 01/2022

    @Description:       Copy segmentation files to corresponding patient folder and rearrange the data folder structure
                        in order to separate the patient images and segmentations (in research file formats) in two
                        different folders.
"""
import logging

from .patients_folder_structure.structure import structure_patients_folder
from .logging_tools import logs_file_setup
from .paths_manager.path_generator import PathGenerator
from .settings import *


if __name__ == "__main__":
    # ----------------------------------------------------------------------------------------------------------- #
    #                                          Logs Setup                                                         #
    # ----------------------------------------------------------------------------------------------------------- #
    logs_file_setup(logging.INFO)

    # ----------------------------------------------------------------------------------------------------------- #
    #                                             Path Generator                                                  #
    # ----------------------------------------------------------------------------------------------------------- #
    path_generator = PathGenerator(
        path_to_patients_folder=PathName.PATH_TO_PATIENTS_FOLDER,
        path_to_segmentations_folder=PathName.PATH_TO_SEGMENTATIONS_FOLDER,
        verbose=True
    )

    # ----------------------------------------------------------------------------------------------------------- #
    #            Copy segmentation files to corresponding patient folder and rearrange file structure             #
    # ----------------------------------------------------------------------------------------------------------- #
    structure_patients_folder(
        path_generator=path_generator,
        patient_images_folder_name=FolderName.PATIENT_IMAGES_FOLDER,
        patient_segmentations_folder_name=FolderName.PATIENT_SEGMENTATIONS_FOLDER
    )
