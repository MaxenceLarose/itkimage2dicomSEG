"""
    @file:              structure.py
    @Author:            Maxence Larose

    @Creation Date:     01/2022
    @Last modification: 01/2022

    @Description:       This file contains the destructure_data_folder function which is used to copy segmentation files
                        to the corresponding patient folder and rearrange the file structure in order to separate the
                        patient images and segmentations (in research file formats) in two different folders.
"""

import os
import shutil

from src.paths_manager.path_generator import PathGenerator


def structure_data_folder(
        path_generator: PathGenerator,
        patient_images_folder_name: str,
        patient_segmentations_folder_name: str
) -> None:
    """
    Copy segmentation files to corresponding patient folder and rearrange file structure in order to separate the
    patient images and segmentations (in research file formats) in two different folders.

    Parameters
    ----------
    path_generator : PathGenerator.
        A PathGenerator object. This object defines, for all patients, the path to the folder containing the
        patient's dicom files and the path to the segmentations related to these dicom files.
    patient_images_folder_name : str
        Name of the folder containing a patient DICOM files.
    patient_segmentations_folder_name : str
        Name of the folder containing a patient segmentation files.
    """
    for path in path_generator:

        # Move dicom files to "images" folder in patient folder
        path_to_images_folder = os.path.join(path.path_to_dicom_folder, patient_images_folder_name)
        os.mkdir(path_to_images_folder)
        for path_to_dicom in os.listdir(path.path_to_dicom_folder):
            shutil.move(
                src=os.path.join(path.path_to_dicom_folder, path_to_dicom),
                dst=path_to_images_folder
            )

        # Move segmentation files (itk image format) to "segmentations" folder in patient folder
        path_to_segmentations_folder = os.path.join(path.path_to_dicom_folder, patient_segmentations_folder_name)
        os.mkdir(path_to_segmentations_folder)
        for path_to_segmentation in path.paths_to_segmentations:
            shutil.copy(
                src=path_to_segmentation,
                dst=path_to_segmentations_folder,
            )
