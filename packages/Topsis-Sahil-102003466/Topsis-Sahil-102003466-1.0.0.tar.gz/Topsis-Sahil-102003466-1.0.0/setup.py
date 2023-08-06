import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="Topsis-Sahil-102003466",
    version="1.0.0",
    description="TOPSIS is a practical and useful technique for ranking and selection of a number of externally determined alternatives through distance measures.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/sahilkadiyan/Topsis-Sahil-102003466.git",
    author="Sahil Kadiyan",
    author_email="kadiyans990@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["Topsis_Sahil_102003466"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "Topsis_Sahil_102003466=Topsis_Sahil_102003466.__main__:main",
        ]
    },
)