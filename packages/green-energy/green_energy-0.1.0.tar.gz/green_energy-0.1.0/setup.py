"""Package setup"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="green_energy",
    version="0.2.0",
    author="",
    author_email="",
    description="A Python API for receiving energy prices from the Awattar API",
    license="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    provides=["green_energy"],
    install_requires=["requests"],
    setup_requires=["wheel"],
)
