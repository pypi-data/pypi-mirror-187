import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="Topsis-Sidharth-102003395",
    version="0.1",
    description="Implements topsis on the given input data file and generates topsis score and ranks accordingly.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/hsurap/Topsis-Sidharth-102003404",
    author="S Sidharth",
    author_email="ssidharth_be20@thapar.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    packages=["topsis"],
    include_package_data=True,
    install_requires=['pandas'],
    entry_points={
        "console_scripts": [
            "topsis=topsis.__main__:main",
        ]
    },
)