"""
    @file:              create_dicom_seg_files.py
    @Author:            Maxence Larose

    @Creation Date:     01/2022
    @Last modification: 01/2022

    @Description:       Create DICOM SEG files from segmentations files in the research data file formats (such as NRRD,
                        NIfTI, etc.).
"""
import logging
import os

from logging_tools import logs_file_setup
from settings import *
from src.dicom_seg.dicom_seg_writer import DicomSEGWriter

if __name__ == "__main__":
    # ----------------------------------------------------------------------------------------------------------- #
    #                                               Logs Setup                                                    #
    # ----------------------------------------------------------------------------------------------------------- #
    logs_file_setup(logging.INFO)

    # ----------------------------------------------------------------------------------------------------------- #
    #                                             Write DICOM SEG                                                 #
    # ----------------------------------------------------------------------------------------------------------- #
    for patient_folder in os.listdir(PathName.PATH_TO_PATIENTS_FOLDER):
        path_to_patient_folder = os.path.join(PathName.PATH_TO_PATIENTS_FOLDER, patient_folder)

        dicom_writer = DicomSEGWriter(
            path_to_dicom_folder=os.path.join(path_to_patient_folder, FolderName.PATIENT_IMAGES_FOLDER),
            path_to_segmentations_folder=os.path.join(path_to_patient_folder, FolderName.PATIENT_SEGMENTATIONS_FOLDER),
            path_to_metadata_json=PathName.PATH_TO_METADATA_JSON
        )

        dicom_writer.write()
