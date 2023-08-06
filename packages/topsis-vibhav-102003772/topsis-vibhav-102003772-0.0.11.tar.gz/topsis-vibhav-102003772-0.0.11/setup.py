import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="topsis-vibhav-102003772",
    version="0.0.11",
    description="It finds topsis for the given data in csv file",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/vibhav10/topsis-package",
    author="Vibhav Shukla",
    author_email="vibhav.1507@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["topsis-vibhav"],
    include_package_data=True,
    install_requires=["pandas", "numpy"],
    entry_points={
        "console_scripts": [
            "topsis_vibhav=topsis_vibhav.__main__:main",
        ]
    },
)