from time import time
import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    setuptools.setup(
    name="CnkiPythonMeta",
    version="0.0.0",
    author="YANG Guixian",
    author_email="Ygxyoung@hotmail.com",
    description="This is a CnkiPythonMeta package for processing data from CNKI(https://www.cnki.net/), which the file type must be EXT format.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
)