import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="Topsis_Meghna_102003663",
    version="0.0.0",
    description="Topsis Implementation",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/meghna3107/Topsis-meghna-102003663.git",
    author="meghna",
    author_email="mmeghna_be20@thapar.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["topsis"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "topsis=topsis.__main__:main",
        ]
    },
)
