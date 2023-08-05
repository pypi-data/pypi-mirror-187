from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='Topsis-Ayush-102016100',
    version='0.0.1',
    description='A python package to implement TOPSIS on a given dataset',
    author= 'Ayush Nagpure',
    url = 'https://github.com/Jubbu05/Topsis-Ayush-102016100',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    keywords=['topsis', 'thapar', '102016100'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=['Topsis-Ayush-102016100'],
    package_dir={'':'src'},
    install_requires = [
    ]
)