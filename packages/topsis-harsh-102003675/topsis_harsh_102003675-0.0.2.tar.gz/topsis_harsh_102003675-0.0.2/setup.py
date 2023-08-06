from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
name='topsis_harsh_102003675',
version='0.0.2',
description='A python package to implement topsis',
author= 'Harsh Paba',
long_description=long_description,
long_description_content_type="text/markdown",
packages=setuptools.find_packages(),
keywords=['topsis', 'maths', 'multiple criteria decision making'],
classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
],
python_requires='>=3.6',
py_modules=['numpy','pandas','logging'],
package_dir={'':'src'},
install_requires = [
    'numpy',
    'pandas',
]
)