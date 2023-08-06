from setuptools import setup
import pathlib
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(name="Topsis_Aditya_102053005",
version="0.16",
description="This is a package for implementing Topsis",
long_description=README,
long_description_content_type="text/markdown",
url = "https://github.com/Adityakalhan/102053005-Aditya-Topsis",
license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
author="Aditya Kalhan",
packages=["Topsis_Aditya_102053005"],
install_requires = ['pandas'],
entry_points={
    "console_scripts" : [
    "102053005=Topsis_Aditya_102053005.topsis:main",
    ]
},
)