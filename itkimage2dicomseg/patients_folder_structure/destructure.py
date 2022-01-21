"""
    @file:              destructure.py
    @Author:            Maxence Larose

    @Creation Date:     01/2022
    @Last modification: 01/2022

    @Description:       This file contains the destructure_data_folder function which is used to rearrange the file
                        structure so that a patient folder contains all DICOMs (including SEG) related to this single
                        patient.
"""

import os
import shutil


def destructure_patients_folder(
        path_to_patients_folder: str,
        patient_images_folder_name: str,
        patient_segmentations_folder_name: str,
        delete_segmentations: bool = False
):
    """
    Rearrange the file structure so that a patient folder contains all DICOMs (including SEG) related to this single
    patient.

    Parameters
    ----------
    path_to_patients_folder : str
        Path to the folder containing all patients folder.
    patient_images_folder_name : str
        Name of the folder containing a patient DICOM files.
    patient_segmentations_folder_name : str
        Name of the folder containing a patient segmentation files.
    delete_segmentations : bool
        Delete the segmentations folder. USE WITH CAUTION!
    """
    for path in os.listdir(path_to_patients_folder):
        path_to_patient_folder = os.path.join(path_to_patients_folder, path)

        path_to_segmentations_folder = os.path.join(path_to_patient_folder, patient_segmentations_folder_name)
        if delete_segmentations:
            shutil.rmtree(path_to_segmentations_folder)
        else:
            for seg_path in os.listdir(path_to_segmentations_folder):
                shutil.move(
                    src=os.path.join(path_to_segmentations_folder, seg_path),
                    dst=path_to_patient_folder
                )
            os.rmdir(path_to_segmentations_folder)

        path_to_images_folder = os.path.join(path_to_patient_folder, patient_images_folder_name)
        for dicom_path in os.listdir(path_to_images_folder):
            shutil.move(
                src=os.path.join(path_to_images_folder, dicom_path),
                dst=path_to_patient_folder
            )
        os.rmdir(path_to_images_folder)
