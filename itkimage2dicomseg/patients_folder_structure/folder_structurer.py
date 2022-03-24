"""
    @file:              folder_structurer.py
    @Author:            Maxence Larose

    @Creation Date:     03/2022
    @Last modification: 03/2022

    @Description:       This file contains the FolderStructurer class which is used to rearrange the patients folders
                        structure so that a patient folder contains an "images" folder containing all the DICOM files
                        and a "segmentations" folder containing all the segmentation files.
"""

import os
import shutil
from typing import NamedTuple

import pydicom

from ..paths_manager.path_generator import PathGenerator


class ImagesFolderStructure(NamedTuple):
    AllInOne: str = "All In One"
    PatientStudySeriesInstanceHierarchy: str = "Patient-Study-Series-Instance Hierarchy"


class SegmentationFilesLocation(NamedTuple):
    AllInOneFolder: str = "All In One Folder"
    InEachPatientFolder: str = "In Each Patient Folder"


class FolderStructurer:
    def __init__(
            self,
            images_folder_structure: str,
            segmentations_files_location: str,
            path_to_patients_folder: str,
            patient_images_folder_name: str,
            patient_segmentations_folder_name: str
    ) -> None:
        """
        Class constructor.

        Just to make everything clear, we present here the 4 possible structure categories.

        CATEGORY 1
        ----------
        - This is the structure we need!
        - ImagesFolderStructure = "All In One"
        - SegmentationFilesLocation = "In Each Patient Folder"
        - Structure diagram :

            |_📂 Patients/
              |_📂 patient1/
                |_📂 images/
                  |_📄 IM0.DCM
                  |_📄 IM1.DCM
                  |_📄 ...
                |_📂 segmentations/
                  |_📄 CT_seg.nrrd
                  |_📄 PET_seg.nii
                  |_📄 ...
              |_📂 patient2/
                |_📂 images/
                  |_📄 IM0.DCM
                  |_📄 ...
                |_📂 segmentations/
                  |_📄 CT.nrrd
                  |_📄 ...
              |_📂 ...

        CATEGORY 2
        ----------
        - ImagesFolderStructure = "All In One"
        - SegmentationFilesLocation = "All In One Folder"
        - Structure diagram :

            |_📂 Patients/
              |_📂 patient1/
                |_📄 IM0.DCM
                |_📄 IM1.DCM
                |_📄 ...
              |_📂 patient2/
                |_📄 IM0.DCM
                |_📄 IM1.DCM
                |_📄 ...
              |_📂 ...
            |_📂 Segmentations/
              |_📄 Patient1_CT.seg.nrrd
              |_📄 Patient1_PET.nrrd
              |_📄 Patient2_CT.nrrd
              |_📄 ...

        CATEGORY 3
        ----------
        - ImagesFolderStructure = "Patient-Study-Series-Instance Hierarchy"
        - SegmentationFilesLocation = "All In One Folder"
        - Structure diagram :

            |_📂 Patients/
              |_📂 patient1/
                |_📂 images/
                  |_📂 study0/
                    |_📂 series0/
                      |_📄 CT0.dcm
                      |_📄 CT1.dcm
                      |_📄 ...
                    |_📂 series1/
                      |_📄 ...
              |_📂 patient2/
                |_📄 ...
              |_📂 patient.../
            |_📂 Segmentations/
              |_📄 Patient1_CT.seg.nrrd
              |_📄 Patient1_PET.nrrd
              |_📄 Patient2_CT.nrrd
              |_📄 ...

        CATEGORY 4
        ----------
        - NOT IMPLEMENTED!!!
        - ImagesFolderStructure = "Patient-Study-Series-Instance Hierarchy"
        - SegmentationFilesLocation = "In Each Patient Folder"
        - Structure diagram :

            |_📂 Patients/
              |_📂 patient1/
                |_📂 images/
                  |_📂 study0/
                    |_📂 series0/
                      |_📄 CT0.dcm
                      |_📄 CT1.dcm
                      |_📄 ...
                    |_📂 series1/
                      |_📄 ...
                |_📂 segmentations/
                  |_📄 CT_seg.nrrd
                  |_📄 PET_seg.nii
                  |_📄 ...
              |_📂 patient2/
                |_📄 ...
              |_📂 patient.../

        Parameters
        ----------
        images_folder_structure: str
            Images folder structure.
        segmentations_files_location: str
            Segmentations files location.
        path_to_patients_folder : str
            Path to the folder containing all patients folder.
        patient_images_folder_name : str
            Name of the folder containing a patient DICOM files.
        patient_segmentations_folder_name : str
            Name of the folder containing a patient segmentation files.
        """
        self._images_structure_category = images_folder_structure
        self._segmentations_structure_category = segmentations_files_location

        self._path_to_patients_folder = path_to_patients_folder
        self._patient_images_folder_name = patient_images_folder_name
        self._patient_segmentations_folder_name = patient_segmentations_folder_name

    def structure(
            self,
            path_to_segmentations_folder: str
    ) -> None:
        """
        Structure all patients folder to the prescribed structure, i.e. an "All In One" images folder structure and a
        "In each patient folder" segmentations folder structure.

        Parameters
        ----------
        path_to_segmentations_folder : str
            Path to the folder containing the segmentations files of all patients.
        """
        if self._segmentations_structure_category == SegmentationFilesLocation.InEachPatientFolder:
            if self._images_structure_category == ImagesFolderStructure.AllInOne:
                pass
            elif self._images_structure_category == ImagesFolderStructure.PatientStudySeriesInstanceHierarchy:
                raise NotImplementedError
        elif self._segmentations_structure_category == SegmentationFilesLocation.AllInOneFolder:
            if self._images_structure_category == ImagesFolderStructure.AllInOne:
                pass
            elif self._images_structure_category == ImagesFolderStructure.PatientStudySeriesInstanceHierarchy:
                self._destructure_images()

            path_generator = PathGenerator(
                path_to_patients_folder=self._path_to_patients_folder,
                path_to_segmentations_folder=path_to_segmentations_folder
            )

            self._structure_segmentations(
                path_generator=path_generator
            )

    def destructure(
            self,
            delete_segmentations: bool = False
    ) -> None:
        """
        Transform all patients images folder to their original structure, i.e. the folder structure they had before
        using the self._structure method. HOWEVER, note that the segmentation files will stay in the "In Each Patient
        Folder" configuration.

        Parameters
        ----------
        delete_segmentations : bool
            True to delete segmentations else False.
        """
        if self._segmentations_structure_category == SegmentationFilesLocation.InEachPatientFolder:
            if self._images_structure_category == ImagesFolderStructure.AllInOne:
                self._destructure_segmentations(delete_segmentations=delete_segmentations)
            elif self._images_structure_category == ImagesFolderStructure.PatientStudySeriesInstanceHierarchy:
                raise NotImplementedError
        elif self._segmentations_structure_category == SegmentationFilesLocation.AllInOneFolder:
            self._destructure_segmentations(delete_segmentations=delete_segmentations)

            if self._images_structure_category == ImagesFolderStructure.AllInOne:
                pass
            elif self._images_structure_category == ImagesFolderStructure.PatientStudySeriesInstanceHierarchy:
                self._structure_images()

    def _structure_segmentations(
            self,
            path_generator: PathGenerator,
    ) -> None:
        """
        Copies segmentation files to corresponding patient folder and rearrange file structure in order to separate the
        patient images and segmentations (in research file formats) in two different folders.

        Parameters
        ----------
        path_generator : PathGenerator.
            A PathGenerator object. This object defines, for all patients, the path to the folder containing the
            patient's dicom files and the path to the segmentations related to these dicom files.
        """
        for path in path_generator:

            # Move dicom files to "images" folder in patient folder
            path_to_images_folder = os.path.join(path.path_to_dicom_folder, self._patient_images_folder_name)
            os.mkdir(path_to_images_folder)
            for path_to_dicom in os.listdir(path.path_to_dicom_folder):
                shutil.move(
                    src=os.path.join(path.path_to_dicom_folder, path_to_dicom),
                    dst=path_to_images_folder
                )

            # Move segmentation files (itk image format) to "segmentations" folder in patient folder
            path_to_segmentations_folder = os.path.join(
                path.path_to_dicom_folder,
                self._patient_segmentations_folder_name
            )

            os.mkdir(path_to_segmentations_folder)
            for path_to_segmentation in path.paths_to_segmentations:
                shutil.copy(
                    src=path_to_segmentation,
                    dst=path_to_segmentations_folder,
                )

    def _destructure_segmentations(
            self,
            delete_segmentations: bool = False
    ):
        """
        Rearranges the file structure so that a patient folder contains all DICOMs (including SEG) related to this
        single patient.

        Parameters
        ----------
        delete_segmentations : bool
            Delete the segmentations folder. USE WITH CAUTION!
        """
        for path in os.listdir(self._path_to_patients_folder):
            path_to_patient_folder = os.path.join(self._path_to_patients_folder, path)

            path_to_segmentations_folder = os.path.join(path_to_patient_folder, self._patient_segmentations_folder_name)
            if delete_segmentations:
                shutil.rmtree(path_to_segmentations_folder)
            else:
                for seg_path in os.listdir(path_to_segmentations_folder):
                    shutil.move(
                        src=os.path.join(path_to_segmentations_folder, seg_path),
                        dst=path_to_patient_folder
                    )
                os.rmdir(path_to_segmentations_folder)

            path_to_images_folder = os.path.join(path_to_patient_folder, self._patient_images_folder_name)
            for dicom_path in os.listdir(path_to_images_folder):
                shutil.move(
                    src=os.path.join(path_to_images_folder, dicom_path),
                    dst=path_to_patient_folder
                )
            os.rmdir(path_to_images_folder)

    def _structure_images(self) -> None:
        """
        Takes a folder containing all DICOMs related to a single patient and restructure it in order to follow the
        patient-study-series-instance hierarchy. In other words patient folder will contain study folders that will
        have series folders inside. Finally, the series will contain the DICOM files representing the instances.
        """
        for path in os.listdir(self._path_to_patients_folder):
            path_to_patient_folder = os.path.join(self._path_to_patients_folder, path)
            study_dict = {}
            series_dict = {}

            it_study = 1
            it_series = 1
            for files in os.listdir(path_to_patient_folder):
                file_path = os.path.join(path_to_patient_folder, files)
                dicom = pydicom.dcmread(file_path)
                study_uid = str(dicom.StudyInstanceUID)
                series_uid = str(dicom.SeriesInstanceUID)

                if study_uid not in study_dict.keys():
                    study_dict[study_uid] = it_study
                    os.makedirs(os.path.join(path_to_patient_folder, f"study{study_dict[study_uid]}"))
                    it_study += 1

                if series_uid not in series_dict.keys():
                    series_dict[series_uid] = it_series
                    os.makedirs(os.path.join(path_to_patient_folder, f"study{study_dict[study_uid]}",
                                             f"series{series_dict[series_uid]}"))
                    it_series += 1

                shutil.move(file_path, os.path.join(path_to_patient_folder, f"study{study_dict[study_uid]}",
                                                    f"series{series_dict[series_uid]}"))

    def _destructure_images(self) -> None:
        """
        Takes a patient folder structured to follow the patient-study-series-instance hierarchy and places all
        instances at the higher level. This method does exactly the opposite of self._structure_images.
        """
        for path in os.listdir(self._path_to_patients_folder):
            path_to_patient_folder = os.path.join(self._path_to_patients_folder, path)
            file_idx = 0
            for study_folder in os.listdir(path_to_patient_folder):
                study_folder_path = os.path.join(path_to_patient_folder, study_folder)
                for series_folder in os.listdir(study_folder_path):
                    series_folder_path = os.path.join(study_folder_path, series_folder)
                    for dicoms in os.listdir(series_folder_path):
                        dicom_path = os.path.join(series_folder_path, dicoms)
                        shutil.move(dicom_path, path_to_patient_folder)
                        os.rename(
                            os.path.join(path_to_patient_folder, dicoms),
                            os.path.join(path_to_patient_folder, f"IM{file_idx}")
                        )
                        file_idx += 1
                    if len(os.listdir(series_folder_path)) != 0:
                        raise ValueError
                    shutil.rmtree(series_folder_path)  # If so, delete it

                if len(os.listdir(study_folder_path)) != 0:
                    raise ValueError
                shutil.rmtree(study_folder_path)

