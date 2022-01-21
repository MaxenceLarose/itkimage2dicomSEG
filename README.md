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

It is important to configure the directory structure correctly to ensure that the module interacts correctly with the data files. The repository, particularly the data folder, must be structured as follows. *The names of the folders and files can and probably will differ, but they must be consistent with the names written in the* `settings.py` *file.*

```
THE DATA FOLDER NEEDS TO BE STRUCTURED AS FOLLOWS :
|_📂 Project directory/
  |_📂 data/
    |_📄 metadata.json
    |_📂 Patients/
      |_📂 patient1/
       	|_📂 images/
       	  |_📄 IM0.DCM
       	  |_📄 IM1.DCM
       	  |_📄 ...
       	|_📂 segmentations/
       	  |_📄 seg1.nrrd
       	  |_📄 seg2.nii
       	  |_📄 ...
      |_📂 patient2/
       	|_📂 images/
       	  |_📄 IM0.DCM
       	  |_📄 ...
       	|_📂 segmentations/
       	  |_📄 seg1.nrrd
       	  |_📄 ...
      |_📂 ...
  |_📄 settings.py
  |_📄 create_dicom_seg_files.py
  |_📄 structure_data_folder.py
  |_📄 destructure_data_folder.py
```

If your data folder is currently structured as presented above, you can skip the [Structure your data directory](#structure-your-data-directory-optional) section below and go directly to [File names](#file-names) section. 

##### Structure your data directory (Optional)

This module provides a way to structure you data directory as presented above, but this part of the code is not very flexible. In fact, the `structure_data_folder.py` script will only work if your data directory structure is as follows. *Again, the names of the folders and files can and probably will differ, but they must be consistent with the names written in the* `settings.py` *file.*

```
IF THE DATA FOLDER IS STRUCTURED AS FOLLOWS, THE structure_data_folder.py SCRIPT CAN BE USED TO REARRANGE THE FOLDER STRUCTURE.
|_📂 Project directory/
  |_📂 data/
    |_📄 metadata.json
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
      |_📄 Patient1_TEP.nrrd
      |_📄 Patient2_CT.nrrd
      |_📄 Patient3_US.nrrd
      |_📄 ...
  |_📄 settings.py
  |_📄 create_dicom_seg_files.py
  |_📄 data_structure_preprocessing.py
  |_📄 ...
```

Here, there is **1 rule** to follow when naming segmentation files. In fact, a strong assumption that is made is that the DICOM data have been previously anonymized. We therefore assume that each patient's name contains a **unique number**.  Segmentation file names must contain this number in order to be able to associate a segmentation with the corresponding patient. To make it easier to find this number in the name of the segmentation file, a word common to all segmentations should be defined and placed in front of the patient number in the name of the segmentation file.  An example of a **patient number prefix** is just the word `Patient`. 

#### File names

It is good practice to create a class that lists the various names and important paths of the folders that contain the data. I propose here a way to organize this class. This allows the user to have an overview of the parameters to be defined and it will also simplify the explanations in the next section on the structure of the data file. 

To do this, it is first necessary to populate the file named `settings.py` which contains the important  `FileName` ,`FolderName` and `PathName` classes.  The `settings.py` file must be placed in the same folder as the `data` folder. It is easier to understand this step with an example so here is the expected content of `settings.py `. *The names of the folders and files can differ.*

```python
from os.path import abspath, dirname, join

ROOT = abspath(dirname(__file__))


class FileName:
    METADATA_JSON: str = "metadata.json"


class FolderName:
    DATA_FOLDER: str = "data"
    PATIENTS_FOLDER: str = "Patients"
    SEGMENTATIONS_FOLDER: str = "Segmentations"  # This folder name is only necessary if you need to restructure your data folder, and therefore, use the function structure_data_folder().
    PATIENT_IMAGES_FOLDER: str = "images"
    PATIENT_SEGMENTATIONS_FOLDER: str = "segmentations"


class PathName:
    PATH_TO_DATA_FOLDER: str = join(ROOT, FolderName.DATA_FOLDER)

    PATH_TO_METADATA_JSON: str = join(PATH_TO_DATA_FOLDER, FileName.METADATA_JSON)
    PATH_TO_PATIENTS_FOLDER: str = join(PATH_TO_DATA_FOLDER, FolderName.PATIENTS_FOLDER)
    PATH_TO_SEGMENTATIONS_FOLDER: str = join(PATH_TO_DATA_FOLDER, FolderName.SEGMENTATIONS_FOLDER)

```

### Use the code

#### Step 1 : Structure your data folder ("Optional"... see [Organize your data](#organize-your-data))

Here, we show the code available in the `structure_data_folder.py` script, which is used to structure the data folder in order to separate the patient images and segmentations in two different folders.

```python
import logging

from itkimage2dicomseg import structure_data_folder, PathGenerator
from itkimage2dicomseg.logging_tools import logs_file_setup

from settings import *

if __name__ == "__main__":
    logs_file_setup(logging.INFO)

    path_generator = PathGenerator(
        path_to_patients_folder=PathName.PATH_TO_PATIENTS_FOLDER,
        path_to_segmentations_folder=PathName.PATH_TO_SEGMENTATIONS_FOLDER,
        verbose=True,
        patient_number_prefix="Patient"
    )

    structure_data_folder(
        path_generator=path_generator,
        patient_images_folder_name=FolderName.PATIENT_IMAGES_FOLDER,
        patient_segmentations_folder_name=FolderName.PATIENT_SEGMENTATIONS_FOLDER
    )

```

#### Step 2 : Create DICOM SEG files

Here, we show the code available in the `create_dicom_seg_files.py` script, which is used to create DICOM SEG files from segmentations files in the research data file formats (such as NRRD, NIfTI, etc.).

```python
import logging
import os

from itkimage2dicomseg import DicomSEGWriter
from itkimage2dicomseg.logging_tools import logs_file_setup

from settings import *

if __name__ == "__main__":
    logs_file_setup(logging.INFO)

    for patient_folder in os.listdir(PathName.PATH_TO_PATIENTS_FOLDER):
        path_to_patient_folder = os.path.join(PathName.PATH_TO_PATIENTS_FOLDER, patient_folder)

        dicom_writer = DicomSEGWriter(
            path_to_dicom_folder=os.path.join(path_to_patient_folder, FolderName.PATIENT_IMAGES_FOLDER),
            path_to_segmentations_folder=os.path.join(path_to_patient_folder, FolderName.PATIENT_SEGMENTATIONS_FOLDER),
            path_to_metadata_json=PathName.PATH_TO_METADATA_JSON
        )

        dicom_writer.write(delete_itk_segmentation_files=False) # You might want to set the variable delete_itk_segmentation_files to True if you want to delete the segmentations.

```

#### Step 3 : Destructure your data folder (Optional)

Here, we show the code available in the `destructure_data_folder.py` script, which is used to rearrange the data folder structure so that a patient folder contains all of his DICOM files, including the newly created DICOM SEG files.

```python
import logging

from itkimage2dicomseg import destructure_data_folder
from itkimage2dicomseg.logging_tools import logs_file_setup

from settings import *

if __name__ == "__main__":
    logs_file_setup(logging.INFO)

    destructure_data_folder(
        path_to_patients_folder=PathName.PATH_TO_PATIENTS_FOLDER,
        patient_images_folder_name=FolderName.PATIENT_IMAGES_FOLDER,
        patient_segmentations_folder_name=FolderName.PATIENT_SEGMENTATIONS_FOLDER
    )

```

## Contact

Maxence Larose, B. Ing., [maxence.larose.1@ulaval.ca](mailto:maxence.larose.1@ulaval.ca)
