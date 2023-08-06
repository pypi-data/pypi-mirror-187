from setuptools import setup
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="Topsis_Taruna_102003464",
version ="0.3",
description ="This is package for topsis of version 0.3",
long_description=long_description,
    long_description_content_type="text/markdown",
author="Taruna Jain",
author_email="tjain_be20@thapar.edu",
packages=['Topsis_Taruna_102003464'],
install_requires=['pandas'],
include_package_data=True,
    entry_points={
            "console_scripts": [
                "topsis123=Topsis_Taruna_102003464.topsis:main",
            ]
    }
)

