import pathlib
from setuptools import setup,find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
with open('README.md', encoding="utf8") as file:
    README = file.read()

# This call to setup() does all the work
setup(
    name="Topsis-Noordeep-102017145",
    version="1.0.0.2",
    description="A Python package for handling problems of Multiple Criteria Decision Making(MCDM) for a given dataset.",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Noordeep Kaur",
    author_email="noordeep29oct@gmail.com",

    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["Topsis"],
    include_package_data=True,
    
    install_requires=['numpy','pandas'],
    entry_points={
        "console_scripts": [
            "topsis=Topsis.Topsis:main",
        ]
     },
   
)