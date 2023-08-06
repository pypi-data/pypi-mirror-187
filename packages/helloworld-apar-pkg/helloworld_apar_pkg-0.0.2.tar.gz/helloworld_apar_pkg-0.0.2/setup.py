from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="helloworld_apar_pkg",
    version="0.0.2",
    author="Apar Garg",
    author_email="aparworkstuff@gmail.com",
    description="Say hello!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/AparGarg99/helloworldpypi",
    install_requires = [
        "blessings ~= 1.7",
        ]
)