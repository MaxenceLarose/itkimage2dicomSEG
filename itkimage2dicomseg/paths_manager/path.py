"""
    @file:              path.py
    @Author:            Maxence Larose

    @Creation Date:     01/2022
    @Last modification: 03/2022

    @Description:       This file contains the Path class.
"""

import os
from typing import Optional, List

from .segmentation_filename_patterns_matcher import SegmentationFilenamePatternsMatcher
from ..utils import get_dicom_header


class Path:
    """
    A class to represent a Path object.
    """

    def __init__(
            self,
            path_to_dicom_folder: str,
            path_to_segmentations_folder: str,
            verbose: bool
    ):
        """
        Used to initialize all the attributes.

        Parameters
        ----------
        path_to_dicom_folder : str
            Path to the folder containing the patient dicom files.
        path_to_segmentations_folder : str
            Path to the folder containing the segmentation files.
        verbose : bool
            True to log/print some information else False.
        """
        self._path_to_dicom_folder = path_to_dicom_folder
        self._path_to_segmentations_folder = path_to_segmentations_folder
        self._verbose = verbose
        self._set_paths_to_segmentations()

    @property
    def path_to_dicom_folder(self) -> str:
        """
        Path to dicom folder property.

        Returns
        -------
        path_to_dicom_folder : str
            Path to the folder containing the patient dicom files.
        """
        return self._path_to_dicom_folder

    @property
    def paths_to_segmentations(self) -> Optional[List[str]]:
        """
        Paths to segmentations.

        Returns
        -------
        path_to_segmentations : Optional[List[str]]
            A list of paths to the segmentation files. The name of the segmentation files must include the series uid of
            their corresponding image, i.e. the image on which the segmentation was made.
        """
        return self._paths_to_segmentations

    def _set_paths_to_segmentations(self) -> None:
        """
        Set paths to segmentations.
        """
        path_to_first_dicom_in_folder = os.path.join(
            self._path_to_dicom_folder,
            os.listdir(self._path_to_dicom_folder)[0]
        )

        dicom_header = get_dicom_header(path_to_dicom=path_to_first_dicom_in_folder)
        patient_id = str(dicom_header.PatientID)

        if self._verbose:
            print(patient_id)

        segmentation_filename_patterns_matcher = SegmentationFilenamePatternsMatcher(
            path_to_segmentations_folder=self._path_to_segmentations_folder,
            patient_id=patient_id
        )

        self._paths_to_segmentations = segmentation_filename_patterns_matcher.get_absolute_paths_to_segmentation_files()
