import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="102003017",
    version="1.0.0",
    description="It finds topsis Score and based on that calculates the rank",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Srishti Sharma",
    author_email="ssharma5_be20@thapar.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["102003017"],
    include_package_data=True,
    install_requires=["pandas", "numpy", "math", "logging", "sys"],
    entry_points={
        "console_scripts": [
            "topsis=topsis.__main__:main",
        ]
    },
)