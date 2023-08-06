import pathlib
from setuptools import setup, find_packages

# The directory containing this file
# HERE = pathlib.Path(_file_).parent

# The text of the README file
with open('README.md', encoding="utf8") as file:
    README = file.read()

# This call to setup() does all the work
setup(
    name="Topsis-Ridhima-102017100",
    version="1.0.0.4",
    description="Python Library that perform TOPSIS",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Ridhima Gupta",
    author_email="600ridhima@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["topsis"],
    include_package_data=True,

    install_requires=['numpy', 'pandas'],
    entry_points={
        "console_scripts": [
            "topsis=topsis.ridhima:main",
        ]
    },

)
