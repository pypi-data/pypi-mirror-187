from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
	name="Topsis-Simardeep-102003559",
	version='1.0.0',
	author='Simardeep Singh',
	author_email='ssingh22_be20@thapar.edu',
	description='Topsis package for Multiple Criteria Decision Making problems(MCDM) problems',
	long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'topsis=Topsis.topsis_simar:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
	)