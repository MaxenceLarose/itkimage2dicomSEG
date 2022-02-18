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

It is important to configure the directory structure correctly to ensure that the module interacts correctly with the data files. The repository, particularly the `Patients` folder, must be structured as follows. *The names of the folders and files can and probably will differ, but they must be consistent with your own folders and files names.*

```
THE PROJECT FOLDER NEEDS TO BE STRUCTURED AS FOLLOWS :
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
  |_📄 create_dicom_seg_files.py
  |_📄 structure_data_folder.py
  |_📄 destructure_data_folder.py
```

If your `Patients` folder is currently structured as presented above, you can skip the [Structure your patients directory](#structure-your-patients-directory-optional) section below and go directly to [Use the code](#use-the-code) section. 

##### Structure your patients directory (Optional)

This module provides a way to structure you data directory as presented above, but this part of the code is not very flexible. In fact, the `structure_patients_folder.py` script will only work if your data directory structure is as follows. *Again, the names of the folders and files can and probably will differ, but they must be consistent with your own folders and files names.*

```
IF THE PROJECT FOLDER IS STRUCTURED AS FOLLOWS, THE structure_patients_folder.py SCRIPT CAN BE USED TO REARRANGE THE FOLDER STRUCTURE.
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
      |_📄 Patient1_PET.nrrd
      |_📄 Patient2_CT.nrrd
      |_📄 Patient3_US.nrrd
      |_📄 ...
  |_📄 create_dicom_seg_files.py
  |_📄 data_structure_preprocessing.py
  |_📄 ...
```

Here, there is **1 rule** to follow when naming segmentation files. In fact, a strong assumption that is made is that the DICOM data have been previously anonymized. We therefore assume that the name of the segmentation files associated with the images of a certain patient contains the ID of that patient. 

### Use the code

#### Step 1 : Structure your data folder ("Optional"... see [Organize your data](#organize-your-data))

Here, we show the code available in the `structure_data_folder.py` script, which is used to structure the data folder in order to separate the patient images and segmentations in two different folders.

```python
import logging

from itkimage2dicomseg import structure_patients_folder, PathGenerator
from itkimage2dicomseg.logging_tools import logs_file_setup

if __name__ == "__main__":
    logs_file_setup(logging.INFO)

    path_generator = PathGenerator(
        path_to_patients_folder="data/Patients",
        path_to_segmentations_folder="data/Segmentations",
        verbose=True
    )

    structure_patients_folder(
        path_generator=path_generator,
        patient_images_folder_name="images",
        patient_segmentations_folder_name="segmentations"
    )

```

#### Step 2 : Create DICOM SEG files

Here, we show the code available in the `create_dicom_seg_files.py` script, which is used to create DICOM SEG files from segmentations files in the research data file formats (such as NRRD, NIfTI, etc.).

```python
import logging
import os

from itkimage2dicomseg import DicomSEGWriter
from itkimage2dicomseg.logging_tools import logs_file_setup

if __name__ == "__main__":
    logs_file_setup(logging.INFO)

    for patient_folder in os.listdir("data/Patients"):
        path_to_patient_folder = os.path.join("data/Patients", patient_folder)

        dicom_writer = DicomSEGWriter(
            path_to_dicom_folder=os.path.join(path_to_patient_folder, "images"),
            path_to_segmentations_folder=os.path.join(path_to_patient_folder, "segmentations"),
            path_to_metadata_json="data/metadata.json"
        )

        dicom_writer.write(delete_itk_segmentation_files=False) # You might want to set the variable delete_itk_segmentation_files to True if you want to delete the segmentations.

```

#### Step 3 : Destructure your data folder (Optional)

Here, we show the code available in the `destructure_data_folder.py` script, which is used to rearrange the data folder structure so that a patient folder contains all of his DICOM files, including the newly created DICOM SEG files.

```python
import logging

from itkimage2dicomseg import destructure_patients_folder
from itkimage2dicomseg.logging_tools import logs_file_setup

if __name__ == "__main__":
    logs_file_setup(logging.INFO)

    destructure_patients_folder(
        path_to_patients_folder="data/Patients",
        patient_images_folder_name="images",
        patient_segmentations_folder_name="segmentations"
    )

```

## Contact

Maxence Larose, B. Ing., [maxence.larose.1@ulaval.ca](mailto:maxence.larose.1@ulaval.ca)
