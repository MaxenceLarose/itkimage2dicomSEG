from setuptools import setup, find_packages

setup(
    name='itkimage2dicomseg',
    version='0.0.2',
    packages=find_packages(),
    long_description=open('README.md', "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url='https://gitlab.chudequebec.ca/MaxenceLarose/itkimage2dicomseg',
    license="Apache License 2.0",
    author='Maxence Larose',
    author_email="maxence.larose.1@ulaval.ca",
    description="Simplify the conversion of segmentation in commonly used research file formats like NRRD and NIfTI "
                "into the standardized DICOM-SEG format. ",
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "grpm-uid @ git+https://gitlab.chudequebec.ca/gacou54/grpm_uid.git",
        "pydicom",
        "pydicom-seg",
    ]
)
