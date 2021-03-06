"""
    @file:              path_generator.py
    @Author:            Maxence Larose

    @Creation Date:     01/2022
    @Last modification: 03/2022

    @Description:       This file contains the PathGenerator class. This class is used to iterate on multiple patients'
                        path to dicom folder to obtain all patients' Path objects. The PathGenerator class inherits from
                        the Generator abstract class.
"""

from collections.abc import Generator
import os

from .path import Path


class PathGenerator(Generator):
    """
    A class used to iterate on multiple patients' path to dicom folder to obtain all patients' Path objects. The
    PathGenerator class inherits from the Generator abstract class.
    """

    def __init__(
            self,
            path_to_patients_folder: str,
            path_to_segmentations_folder: str,
            verbose: bool = False
    ):
        """
        Used to initialize the self.paths_to_patients_dicom_folder attribute.

        Parameters
        ----------
        path_to_patients_folder : str
            Patients folder path.
        path_to_segmentations_folder : str
            Segmentations folder path.
        verbose : bool
            True to print some information else False. (default = False)
        """
        paths_to_patients_dicom_folder = []
        for path_to_patient_folder in os.listdir(path_to_patients_folder):
            path_to_dicom_folder = os.path.join(path_to_patients_folder, path_to_patient_folder)
            paths_to_patients_dicom_folder.append(path_to_dicom_folder)
        self._paths_to_patients_dicom_folder = paths_to_patients_dicom_folder

        self._path_to_segmentations_folder = path_to_segmentations_folder
        self._verbose = verbose
        self.current_index = 0

    def __len__(self) -> int:
        """
        Total number of patients.

        Returns
        -------
        length: int
            Total number of patients.
        """
        return len(self._paths_to_patients_dicom_folder)

    def send(self, _) -> Path:
        """
        Resumes the execution and sends a value into the generator function. This method returns the next value yielded
        by the generator and update the current index or raises StopIteration (via the self.throw method) if all paths
        have been generated.

        Returns
        -------
        path: Path
            Path object.
        """
        if self.current_index == 0:
            if self._verbose:
                print("\nAssociating patient records with their corresponding image segmentation files...")
        elif self.current_index == self.__len__():
            if self._verbose:
                print("Done.")
            self.throw()

        path_to_dicom_folder = self._paths_to_patients_dicom_folder[self.current_index]

        path = Path(
            path_to_dicom_folder=path_to_dicom_folder,
            path_to_segmentations_folder=self._path_to_segmentations_folder,
            verbose=self._verbose
        )

        self.current_index += 1

        return path

    def throw(self, typ=StopIteration, value=None, traceback=None) -> None:
        """
        Raises an exception of type typ.
        """
        raise typ