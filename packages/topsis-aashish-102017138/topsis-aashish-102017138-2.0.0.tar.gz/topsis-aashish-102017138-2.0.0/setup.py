import pathlib
from setuptools import setup,find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="topsis-aashish-102017138",
    version="2.0.0",
    description="This is a Python library for handling problems related to Multiple Criteria Decision Making(MCDM) using TOPSIS algorithm",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/aashish-1904",
    author="Aashish Kumar",
    author_email="aashishkumar19042002@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["topsis"],
    include_package_data=True,   
    install_requires=['numpy','pandas'],
    entry_points={
        "console_scripts": [
            "topsis=topsis.__main__:main",
        ]
     },
   
)