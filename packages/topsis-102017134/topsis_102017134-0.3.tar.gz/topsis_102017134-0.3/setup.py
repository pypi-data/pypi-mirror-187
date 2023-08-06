from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
	name="topsis_102017134",
	version='0.3',
	author='Soumya Srivastava',
	author_email='ssrivastava_be20@thapar.edu',
	description='topsis package for MCDM problems',
	long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sri-soumya/topsis",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'topsisSolve=topsis_102017134.topsis:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
	)