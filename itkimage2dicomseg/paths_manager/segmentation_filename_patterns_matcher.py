"""
    @file:              segmentation_filename_patterns_matcher.py
    @Author:            Maxence Larose

    @Creation Date:     01/2022
    @Last modification: 01/2022

    @Description:       This file contains the SegmentationFilenamePatternsMatcher class whose main purpose is to obtain
                        a list of absolute paths to the segmentation files given the location of the folder containing
                        all the segmentations and the patient ID.
"""

import os
from typing import List

import numpy as np


class SegmentationFilenamePatternsMatcher:
    """
    A class whose main purpose is to obtain a list of absolute paths to the segmentation files given the location of the
    folder containing all the segmentations, the patient name and the patient number prefix used in the name of
    segmentations file.
    """

    def __init__(
            self,
            path_to_segmentations_folder: str,
            patient_id: str
    ):
        """
        Used to initialize all the class' attributes.

        Parameters
        ----------
        path_to_segmentations_folder : str
            Path to the folder containing all segmentations.
        patient_id : str
            Patient ID.
        """
        self.path_to_segmentations_folder = path_to_segmentations_folder
        self.patient_id = patient_id

    @property
    def patient_id(self) -> str:
        """
        Patient ID.

        Returns
        -------
        patient_id : str
            Patient ID.
        """
        return self._patient_id

    @patient_id.setter
    def patient_id(
            self,
            patient_id: str
    ) -> None:
        """
        Set patient name.

        Parameters
        ----------
        patient_id : str
            Patient ID.
        """
        self._patient_id = patient_id

    @property
    def paths_to_segmentation_files(self) -> List[str]:
        """
        Paths to segmentation files.

        Returns
        -------
        paths : List[str]
            A list of all the paths to the segmentation files.
        """
        return os.listdir(self.path_to_segmentations_folder)

    @property
    def matches(self) -> List[bool]:
        """
        Get a boolean list indicating whether or not the segmentation filenames match the pattern defined using the
        patient ID.

        Returns
        -------
        matches : List[bool]
            A list of booleans where the value is True if all the patterns are found in the name of the segmentation
            file and False otherwise. The indexes of the list represents a specific segmentation file (see
            paths_to_segmentation_files).
        """
        matches = [False] * len(self.paths_to_segmentation_files)
        pattern = self.patient_id

        for path_idx, path_to_segmentation_file in enumerate(self.paths_to_segmentation_files):
            if pattern in path_to_segmentation_file:
                pattern_start_idx = path_to_segmentation_file.find(pattern)
                idx_following_pattern = pattern_start_idx + int(len(pattern))
                character_following_pattern = path_to_segmentation_file[idx_following_pattern]

                if not character_following_pattern.isdigit():
                    matches[path_idx] = True

        return matches

    def get_absolute_paths_to_segmentation_files(
            self,
    ) -> List[str]:
        """
        Get the absolute paths of the segmentation files whose filenames match the pattern of the given patient name.

        Returns
        -------
        absolute_paths_to_segmentation : List[str]
            A list of the absolute paths to all the segmentation files whose filenames match the pattern of the given
            patient name.
        """
        paths_to_segmentation_file = [self.paths_to_segmentation_files[i] for i in np.where(self.matches)[0]]

        absolute_paths_to_segmentation = []
        for path_to_segmentations_file in paths_to_segmentation_file:
            absolute_path_to_segmentation = os.path.join(self.path_to_segmentations_folder, path_to_segmentations_file)
            absolute_paths_to_segmentation.append(absolute_path_to_segmentation)

        return absolute_paths_to_segmentation
