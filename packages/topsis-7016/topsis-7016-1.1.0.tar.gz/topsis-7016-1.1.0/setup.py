from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
	name="topsis-7016",
	version='1.1.0',
	author='Mukul Sharda',
	author_email='mukulsharda5@gmail.com',
	description='topsis package for MCDM problems',
	long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    keywords='topsis',
    install_requires=[
        'pandas==1.5.2',
        'numpy>=1.23.3'
    ],
    entry_points={
        'console_scripts': [
            'topsis=topsis.topsis:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
	)