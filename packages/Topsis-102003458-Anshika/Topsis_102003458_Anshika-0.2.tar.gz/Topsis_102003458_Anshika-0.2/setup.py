from setuptools import setup
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="Topsis_102003458_Anshika",
version ="0.2",
description ="This is package for topsis of version 0.1",
long_description=long_description,
    long_description_content_type="text/markdown",
author="Anshika Singla",
author_email="asingla2_be20@thapar.edu",
packages=['Topsis_102003458_Anshika'],
install_requires=['pandas'],
include_package_data=True,
    entry_points={
            "console_scripts": [
                "topsis123=Topsis_102003458_Anshika.topsis:main",
            ]
    }
)

