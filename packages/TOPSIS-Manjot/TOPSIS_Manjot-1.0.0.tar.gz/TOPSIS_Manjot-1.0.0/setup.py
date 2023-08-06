from setuptools import setup, find_packages
import codecs
import os
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="TOPSIS_Manjot",
    version="1.0.0",
    description="Calculates Topsis Score and Rank them accordingly",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/SingManjot/TOPSIS_Manjot",
    author="Manjot Singh Kandhari",
    author_email="smanjot444@gmail.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "topsis=TOPSIS_Manjot.__main__:main",
        ]
    },
)