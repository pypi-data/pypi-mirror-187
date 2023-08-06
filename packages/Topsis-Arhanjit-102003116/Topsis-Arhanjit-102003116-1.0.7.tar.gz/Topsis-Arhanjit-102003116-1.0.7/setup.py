import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="Topsis-Arhanjit-102003116",
    version="1.0.7",
    description="This is a Python library for handling problems related to Multiple Criteria Decision Making(MCDM)",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Arhan2002/Topsis-Arhanjit-102003116.git",
    author="Arhanjit Sodhi",
    author_email="arhanjitsodhi@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["Topsis_Arhanjit_102003116"],
    include_package_data=True,
    install_requires="pandas",
    entry_points={
        "console_scripts": [
            "topsis=Topsis_Arhanjit_102003116.topsis:main",
        ]
    },
)