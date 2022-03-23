"""
    @file:              dicom_seg_writer.py
    @Author:            Maxence Larose

    @Creation Date:     01/2022
    @Last modification: 03/2022

    @Description:       This file contains the DicomSEGWriter which is to create DICOM SEG files from segmentations
                        files in the research data file formats (such as NRRD, NIfTI, etc.).
"""

import pathlib
import os
from typing import List, NamedTuple, Set

from grpm_uid import generate_uid
import pydicom
import pydicom_seg
import SimpleITK as sitk

from ..utils import get_dicom_header


class DicomSEGWriter:

    class SeriesData(NamedTuple):
        """
        Series description namedtuple to simplify management of values.
        """
        series_description: str
        paths_to_dicoms_from_series: List[str]
        dicom_header: pydicom.dataset.FileDataset

    def __init__(
            self,
            path_to_dicom_folder: str,
            path_to_segmentations_folder: str,
            path_to_metadata_json: str
    ):
        """
        Constructor of the class DicomSEGWriter.

        Parameters
        ----------
        path_to_dicom_folder : str
            Path to the folder containing the patient dicom files.
        path_to_segmentations_folder : str
            Path to the folder containing the patient segmentation files in the research data file formats (such as
            NRRD, NIfTI, etc.).
        path_to_metadata_json : str
            In order to do the conversion, we need to pass extra metadata that describe the segmentations to the
            converter. See https://qiicr.gitbook.io/dcmqi-guide/use-cases/freesurfer.
        """
        self._path_to_dicom_folder = path_to_dicom_folder
        self._path_to_segmentations_folder = path_to_segmentations_folder
        self._path_to_metadata_json = path_to_metadata_json

    @property
    def _paths_to_segmentations(self) -> List[str]:
        """
        Paths to segmentations.

        Returns
        -------
        paths_to_segmentations : List[str]
            A list of paths to the segmentation files.
        """
        path_to_segmentations = []
        for path in os.listdir(self._path_to_segmentations_folder):
            path_to_segmentations.append(os.path.join(self._path_to_segmentations_folder, path))
        return path_to_segmentations

    @property
    def __series_ids(self) -> List[str]:
        """
        Get all series IDs from a patient's dicom folder.

        Returns
        -------
        series_ids : List[str]
            All series IDs contained in a patient folder.
        """
        series_reader = sitk.ImageSeriesReader()
        series_ids = series_reader.GetGDCMSeriesIDs(self._path_to_dicom_folder)

        if not series_ids:
            raise FileNotFoundError(f"Given directory {self._path_to_dicom_folder} does not contain a DICOM series.")

        return series_ids

    @property
    def __series_data_list(self) -> List[SeriesData]:
        """
        Get the series data from series IDs and the path to the patient's dicom folder.

        Returns
        -------
        series_data_list : List[DicomSEGWriter.SeriesData]
            List of the data from the selected series.
        """
        series_data_list: List[DicomSEGWriter.SeriesData] = []
        all_patient_uids: Set[str] = set()
        for idx, series_id in enumerate(self.__series_ids):
            series_reader = sitk.ImageSeriesReader()
            paths_to_dicoms_from_series = series_reader.GetGDCMSeriesFileNames(self._path_to_dicom_folder, series_id)

            path_to_first_dicom_of_series = paths_to_dicoms_from_series[0]
            loaded_dicom_header = get_dicom_header(path_to_dicom=path_to_first_dicom_of_series)
            all_patient_uids.add(loaded_dicom_header.PatientID)

            series_data = self.SeriesData(
                series_description=loaded_dicom_header.SeriesDescription,
                paths_to_dicoms_from_series=paths_to_dicoms_from_series,
                dicom_header=loaded_dicom_header
            )
            series_data_list.append(series_data)

        if len(all_patient_uids) != 1:
            raise AssertionError(f"All dicom files in the same folder must belong to the same patient. This is not the "
                                 f"case for the patient whose data is currently being downloaded since the uids "
                                 f"{all_patient_uids} are found in his or her folder.")

        return series_data_list

    @property
    def _template(self) -> pydicom.Dataset:
        """
        Template for the converter metadata.

        Returns
        -------
        template : pydicom.Dataset
            Metadata template.
        """
        return pydicom_seg.template.from_dcmqi_metainfo(self._path_to_metadata_json)

    @staticmethod
    def _display_series_list(series_data_list: List[SeriesData]) -> None:
        """
        Print the patient's UID and its series descriptions (and index).
        """
        print(f"{'-'*50}\nPatient ID : {series_data_list[0].dicom_header.PatientID}")
        for series_idx, series_data in enumerate(series_data_list):
            print(f"Series index: {series_idx}, Series Description: {series_data.series_description}")

    def get_dicom_series_paths_for_given_segmentation(self, path_to_segmentation: str) -> List[str]:
        """
        Print the patient's UID and its series descriptions (and index).

        Parameters
        ----------
        path_to_segmentation : str
            Path to a segmentation file.

        Returns
        -------
        paths_to_dicoms_from_series : List[str]
            List of paths to the DICOMs from the chosen series.
        """
        segmentation_filename = os.path.basename(path_to_segmentation)
        series_data_list = self.__series_data_list

        self._display_series_list(series_data_list=series_data_list)
        chosen_series = None
        while True:
            try:
                series_idx = input(f"Which of the above series contains the source images for the segmentation named "
                                   f"{segmentation_filename}? \nPlease enter the reference series index here:")
                chosen_series = series_data_list[int(series_idx)]
            except IndexError as e:
                print(f"IndexError : {e}. Please enter a valid index. Try again.")
                continue
            except ValueError as e:
                print(f"ValueError : {e}. Please enter an index (integer), not a name. Try again.")
                continue
            break

        return chosen_series.paths_to_dicoms_from_series

    @staticmethod
    def __get_3d_sitk_image_from_dicom_series(
            paths_to_dicoms_from_series: List[str],
    ) -> sitk.Image:
        """
        Get a 3D image array from a list of dicom paths associated to the same series.

        Parameters
        ----------
        paths_to_dicoms_from_series : List[str]
            List of paths to the DICOMs from the chosen series.

        Returns
        -------
        image : sitk.Image
            3D SimpleITK image obtained from the series.
        """
        series_reader = sitk.ImageSeriesReader()
        series_reader.SetFileNames(paths_to_dicoms_from_series)

        image = series_reader.Execute()

        return image

    @staticmethod
    def get_sitk_label_map_for_given_segmentation(path_to_segmentation: str) -> sitk.Image:
        """
        Get the SimpleITK Image from a path to a segmentation.

        Parameters
        ----------
        path_to_segmentation : str
            Path to a segmentation file.

        Returns
        -------
        image : sitk.Image
            Segmentation ITK image.
        """
        file_reader = sitk.ImageFileReader()
        file_reader.SetFileName(fn=path_to_segmentation)
        return file_reader.Execute()

    @staticmethod
    def _resample_mask(
            mask: sitk.Image,
            image: sitk.Image
    ) -> sitk.Image:
        """
        Resample an itk_image to new out_spacing.

        Parameters
        ----------
        mask : sitk.Image
            The input mask.
        image : sitk.Image
            The source image.

        Returns
        -------
        resampled_mask : sitk.Image
            The resampled mask.
        """
        resampled_mask = sitk.Resample(
            image1=mask,
            referenceImage=image,
            transform=sitk.Transform(),
            interpolator=sitk.sitkNearestNeighbor,
            defaultPixelValue=0,
            outputPixelType=mask.GetPixelID()
        )

        return resampled_mask

    @staticmethod
    def is_segmentation_association_process_complete():
        """
        Ask the user if all the source images of the current segmentation have been associated.

        Returns
        -------
        process_complete : bool
            Process complete.
        """
        while True:
            answer = input(
                "Do you want to choose an additional source image for this segmentation? (y/n)"
            )

            if answer == "y" or answer == "n":
                process_complete = answer.lower() in ["n"]
                break
            else:
                print("Try again. Make sure to choose between 'y' or 'n'.")

        return process_complete

    def write(
            self,
            resample_segmentation_to_source_image_size: bool = False,
            delete_itk_segmentation_files: bool = False,
            enable_multi_images_association: bool = False,
            **kwargs
    ):
        """
        Write DICOM SEG files using the segmentation files associated to their source DICOM images.

        Parameters
        ----------
        resample_segmentation_to_source_image_size : bool
            Whether or not to resample mask to source image size.
        delete_itk_segmentation_files : bool
            Delete itk segmentation files after the DICOM-SEG segmentation files are created. USE WITH CAUTION!
        enable_multi_images_association : bool
            Enable association of several images to the same segmentation.
        kwargs : dict
            inplane_cropping : bool, default = False
            skip_empty_slices : bool, default = False
            skip_missing_segment : bool, default = False
        """
        writer = pydicom_seg.MultiClassWriter(
            template=self._template,
            inplane_cropping=kwargs.get("inplane_cropping", False),
            skip_empty_slices=kwargs.get("skip_empty_slices", False),
            skip_missing_segment=kwargs.get("skip_missing_segment", False)
        )

        for path_to_seg in self._paths_to_segmentations:
            process_complete = False
            i = 0
            while not process_complete:
                source_images = self.get_dicom_series_paths_for_given_segmentation(path_to_seg)
                segmentation = self.get_sitk_label_map_for_given_segmentation(path_to_seg)

                if resample_segmentation_to_source_image_size:
                    image = self.__get_3d_sitk_image_from_dicom_series(paths_to_dicoms_from_series=source_images)
                    segmentation = self._resample_mask(mask=segmentation, image=image)

                dcm = writer.write(segmentation, source_images)

                dcm.SOPInstanceUID = generate_uid()
                dcm.SeriesInstanceUID = generate_uid()

                new_path = f"{os.path.join(self._path_to_segmentations_folder, pathlib.Path(path_to_seg).stem)}_" \
                           f"{i}.SEG.dcm"
                dcm.save_as(new_path)

                print(f"DICOM SEG file saved with path {new_path}.\n")

                if enable_multi_images_association:
                    process_complete = self.is_segmentation_association_process_complete()
                    i += 1
                else:
                    process_complete = True

                if delete_itk_segmentation_files and process_complete:
                    os.remove(path_to_seg)
