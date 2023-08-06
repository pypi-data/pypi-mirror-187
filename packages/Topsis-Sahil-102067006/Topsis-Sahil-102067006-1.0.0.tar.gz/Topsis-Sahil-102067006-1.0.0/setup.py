from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
	name="Topsis-Sahil-102067006",
	version='1.0.0',
	author='Sahil Singla',
	author_email='ssingla_be20@thapar.edu',
	description='topsis package for MCDM problems',
	long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sahil1239",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'topsis=topsis.topsis:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
	)

