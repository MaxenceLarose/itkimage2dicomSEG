from setuptools import setup, find_packages

setup(
    name='itkimage2dicomseg',
    version='0.0.1',
    packages=find_packages(),
    url='https://gitlab.chudequebec.ca/MaxenceLarose/itkimage2dicomseg',
    license="Apache License 2.0",
    author='Maxence Larose',
    author_email="maxence.larose.1@ulaval.ca",
    description="Simplify the conversion of segmentation in commonly used research file formats like NRRD and NIfTI "
                "into the standardized DICOM-SEG format. ",
    install_requires=[
        "grpm-uid @ git+https://gitlab.chudequebec.ca/gacou54/grpm_uid.git",
        "pydicom",
        "pydicom-seg",
    ]
)
