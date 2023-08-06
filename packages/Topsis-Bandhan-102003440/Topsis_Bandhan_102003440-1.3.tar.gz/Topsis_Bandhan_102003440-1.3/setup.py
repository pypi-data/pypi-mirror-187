from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="Topsis_Bandhan_102003440",
    version="1.3",
    author="Bandhan Sher Singh",
    author_email="bsingh3_be20@thapar.edu",
    description ="Doing Evaluation of alternatives based on multiple criteria using TOPSIS method.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['Topsis_Bandhan_102003440'],
    install_requires=['pandas'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "topsis=Topsis_Bandhan_102003440.Bandhan_102003440:main",
        ]
    }
    
)