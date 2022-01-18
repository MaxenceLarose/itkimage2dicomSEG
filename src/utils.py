import logging
import os
import shutil

import pydicom

from src.paths_manager.path_generator import PathGenerator


def get_dicom_header(
        path_to_dicom: str,
        show: bool = False
) -> pydicom.dataset.FileDataset:
    """
    Get a dicom header given the path to the dicom.

    Parameters
    ----------
    path_to_dicom : str
        The path to the dicom file.
    show : bool
        Show dicom header in console.

    Returns
    -------
    loaded_dicom : pydicom.dataset.FileDataset
        Loaded DICOM dataset.
    """
    loaded_dicom = pydicom.dcmread(path_to_dicom, stop_before_pixels=True)

    if show:
        logging.info(loaded_dicom)

    return loaded_dicom


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


def destructure_data_folder(
        path_to_patients_folder: str,
        patient_images_folder_name: str,
        patient_segmentations_folder_name: str
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
    """
    for path in os.listdir(path_to_patients_folder):
        path_to_patient_folder = os.path.join(path_to_patients_folder, path)

        path_to_segmentations_folder = os.path.join(path_to_patient_folder, patient_segmentations_folder_name)
        shutil.rmtree(path_to_segmentations_folder)

        path_to_images_folder = os.path.join(path_to_patient_folder, patient_images_folder_name)
        for dicom_path in os.listdir(path_to_images_folder):
            shutil.move(
                src=os.path.join(path_to_images_folder, dicom_path),
                dst=path_to_patient_folder
            )
        os.rmdir(path_to_images_folder)
