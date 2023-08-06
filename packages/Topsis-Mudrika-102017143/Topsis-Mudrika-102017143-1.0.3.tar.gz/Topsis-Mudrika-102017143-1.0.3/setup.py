import pathlib
from setuptools import setup,find_packages

# The directory containing this file


# The text of the README file
with open('README.md', encoding="utf8") as file:
    README = file.read()

# This call to setup() does all the work
setup(
    name="Topsis-Mudrika-102017143",
    version="1.0.3",
    description="This is a Python library for handling problems related to Multiple Criteria Decision Making(MCDM)",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Mudrika Jain",
    author_email="jainmudrika29@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["source"],
    include_package_data=True,
    
    install_requires=['numpy','pandas'],
    entry_points={
        "console_scripts": [
            "topsis=source.func:main",
        ]
     },
   
)