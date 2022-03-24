# ITK images to DICOM-SEG files conversion pipeline

Simplify the conversion of segmentation in commonly used research file formats like NRRD and NIfTI into the standardized  [DICOM-SEG](https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.8.20.html) format. 

## Motivation

The **purpose** of this project is to provide a pipeline that contains the necessary tools to manage paths and references during the conversion of a segmentation in a research file format (`.nrrd`, `.nii`, etc.) to a DICOM-SEG file.  The main goal is accomplished by using the [pydicom-seg](https://pypi.org/project/pydicom-seg/) library to create the DICOM-SEG files.

## Installation

### From GitHub :

```
pip install git+https://github.com/MaxenceLarose/itkimage2dicomSEG.git
```

### From GitLab :

```
pip install git+https://gitlab.chudequebec.ca/MaxenceLarose/itkimage2dicomseg.git
```

## Limitations

A known limitation of the [pydicom-seg](https://pypi.org/project/pydicom-seg/) library is that it can only write multi-class segmentation, which means overlapping segments are not allowed.

## Getting started

### Create a JSON parameter file

A JSON parameter file is necessary so that the segmentation output is described in terms of standardized vocabularies such as [SNOMED](https://en.wikipedia.org/wiki/Systematized_Nomenclature_of_Medicine), and segmentation can be saved in DICOM format side by side and cross-referenced with the source image data. This can help remove ambiguity about the meaning of the results.

All documentation regarding the creation of such a file is available in the [user guide](https://qiicr.gitbook.io/dcmqi-guide/) for the [dcmqi](https://github.com/qiicr/dcmqi) (DICOM for Quantitative Imaging) library. They even provide a [web application](http://qiicr.org/dcmqi/#/seg) to populate the metadata JSON file.

### Organize your data

#### Data Structure

It is important to configure the directory structure correctly to ensure that the module interacts correctly with the data files. The repository, particularly the `Patients` folder, must be structured as follows :

```
# CATEGORY 1 (ImagesFolderStructure = "All In One", SEGMENTATIONS = "In Each Patient Folder") - This is the structure we need!
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
```

If your `Patients` folder is not currently structured as presented above, don't worry. The `FolderStructurer` can automatically transform your folder structure into the prescribed one IF your current structure falls into one of the two categories below.

```
# CATEGORY 2 (IMAGES = "All In One", SEGMENTATIONS = "All In One Folder")
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
```

```
CATEGORY 3 (IMAGES = Patient-Study-Series-Instance Hierarchy, SEGMENTATIONS = "All In One Folder")
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
```

Here, there is **1 rule** to follow when naming segmentation files. In fact, a strong assumption that is made is that the name of the segmentation files associated with the images of a certain patient contains the ID of that patient. 

### Use the code - Create DICOM SEG files

Here, we show the code available in the `example.py` script, which is used to create DICOM SEG files from segmentations files in the research data file formats (such as NRRD, NIfTI, etc.).

```python
import os

from itkimage2dicomseg import DicomSEGWriter
from itkimage2dicomseg.patients_folder_structure import (ImagesFolderStructure, SegmentationFilesLocation,
                                                         FolderStructurer)

from settings import *


if __name__ == "__main__":
    # ----------------------------------------------------------------------------------------------------------- #
    #                                     Initialize folder structurer                                            #
    # ----------------------------------------------------------------------------------------------------------- #
    folder_structurer = FolderStructurer(
        images_structure_category=ImagesFolderStructure.AllInOne,
        segmentations_structure_category=SegmentationFilesLocation.AllInOne,
        path_to_patients_folder="data/Patients",
        patient_images_folder_name="images",
        patient_segmentations_folder_name="segmentations"
    )

    # ----------------------------------------------------------------------------------------------------------- #
    #                                            Structure folder                                                 #
    # ----------------------------------------------------------------------------------------------------------- #
    folder_structurer.structure(path_to_segmentations_folder="data/Segmentations")

    # ----------------------------------------------------------------------------------------------------------- #
    #                                         Create DICOM SEG files                                              #
    # ----------------------------------------------------------------------------------------------------------- #
    for patient_folder in os.listdir(PathName.PATH_TO_PATIENTS_FOLDER):
        path_to_patient_folder = os.path.join("data/Patients", patient_folder)

        dicom_writer = DicomSEGWriter(
            path_to_dicom_folder=os.path.join(path_to_patient_folder, "images"),
            path_to_segmentations_folder=os.path.join(path_to_patient_folder, "segmentations"),
            path_to_metadata_json="data/metadata.json"
        )

        dicom_writer.write(
            resample_segmentation_to_source_image_size=True, 
            delete_itk_segmentation_files=True,
            enable_multi_images_association=True
        )

    # ----------------------------------------------------------------------------------------------------------- #
    #                        "Destructure" folder to original images folder structure                             #
    # ----------------------------------------------------------------------------------------------------------- #
    folder_structurer.destructure()

```

## Contact

Maxence Larose, B. Ing., [maxence.larose.1@ulaval.ca](mailto:maxence.larose.1@ulaval.ca)
