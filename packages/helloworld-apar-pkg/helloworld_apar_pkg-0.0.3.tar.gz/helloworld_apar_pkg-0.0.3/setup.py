from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="helloworld_apar_pkg",
    version="0.0.3",
    author="Apar Garg",
    author_email="aparworkstuff@gmail.com",
    description="Say hello!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/AparGarg99/helloworldpypi",
    install_requires = [
        "tqdm ~= 4.64.1",
        ]
)