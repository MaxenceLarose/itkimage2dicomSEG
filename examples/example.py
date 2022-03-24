"""
    @file:              create_dicom_seg_files.py
    @Author:            Maxence Larose

    @Creation Date:     01/2022
    @Last modification: 03/2022

    @Description:       Create DICOM SEG files from segmentations files in the research data file formats (such as NRRD,
                        NIfTI, etc.).
"""
import env_examples  # Modifies path, DO NOT REMOVE
import os

from itkimage2dicomseg import DicomSEGWriter
from itkimage2dicomseg.patients_folder_structure import (ImagesFolderStructure, SegmentationFilesLocation,
                                                         FolderStructurer)


if __name__ == "__main__":
    # ---------------------------------------------------------------------------------------------------- #
    #                                              Constants                                               #
    # ---------------------------------------------------------------------------------------------------- #
    PATH_TO_METADATA_JSON_FILE = "data/metadata.json"
    PATH_TO_PATIENTS_FOLDER = "data/Patients"
    PATH_TO_SEGMENTATIONS_FOLDER = "data/Segmentations"

    PATIENTS_IMAGES_FOLDER_NAME = "images"
    PATIENTS_SEGMENTATIONS_FOLDER_NAME = "segmentations"

    # ---------------------------------------------------------------------------------------------------- #
    #                                     Initialize folder structurer                                     #
    # ---------------------------------------------------------------------------------------------------- #
    folder_structurer = FolderStructurer(
        images_folder_structure=ImagesFolderStructure.AllInOne,
        segmentations_files_location=SegmentationFilesLocation.AllInOneFolder,
        path_to_patients_folder=PATH_TO_PATIENTS_FOLDER,
        patient_images_folder_name=PATIENTS_IMAGES_FOLDER_NAME,
        patient_segmentations_folder_name=PATIENTS_SEGMENTATIONS_FOLDER_NAME
    )

    # ---------------------------------------------------------------------------------------------------- #
    #                                            Structure folder                                          #
    # ---------------------------------------------------------------------------------------------------- #
    folder_structurer.structure(path_to_segmentations_folder=PATH_TO_SEGMENTATIONS_FOLDER)

    # ---------------------------------------------------------------------------------------------------- #
    #                                         Create DICOM SEG files                                       #
    # ---------------------------------------------------------------------------------------------------- #
    for patient_folder in os.listdir(PATH_TO_PATIENTS_FOLDER):
        path_to_patient_folder = os.path.join(PATH_TO_PATIENTS_FOLDER, patient_folder)

        dicom_writer = DicomSEGWriter(
            path_to_images_folder=os.path.join(path_to_patient_folder, PATIENTS_IMAGES_FOLDER_NAME),
            path_to_segmentations_folder=os.path.join(path_to_patient_folder, PATIENTS_SEGMENTATIONS_FOLDER_NAME),
            path_to_metadata_json=PATH_TO_METADATA_JSON_FILE
        )

        dicom_writer.write(
            resample_segmentation_to_source_image_size=True,
            delete_itk_segmentation_files=True,
            enable_multi_images_association=True
        )

    # ---------------------------------------------------------------------------------------------------- #
    #                        "Destructure" folder to original images folder structure                      #
    # ---------------------------------------------------------------------------------------------------- #
    # folder_structurer.destructure()
