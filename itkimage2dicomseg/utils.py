"""
    @file:              utils.py
    @Author:            Maxence Larose

    @Creation Date:     01/2022
    @Last modification: 01/2022

    @Description:       A collection of functions and classes that may or may not be useful.
"""

import pydicom


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
        print(loaded_dicom)

    return loaded_dicom
