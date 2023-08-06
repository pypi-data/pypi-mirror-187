import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="TopsisSimranjit102017060",
    version="2.0.0",
    description="Python library for dealing with Multiple Criteria Decision Making(MCDM) problems",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/S03imran/Topsis.git",
    author="Simranjit Kaur",
    author_email="s03imran@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["TopsisSimranjit102017060"],
    include_package_data=True,
    install_requires=[],
)