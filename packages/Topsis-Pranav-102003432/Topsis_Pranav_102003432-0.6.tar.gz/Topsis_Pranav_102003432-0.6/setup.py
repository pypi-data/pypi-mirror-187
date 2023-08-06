from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="Topsis_Pranav_102003432",
    version="0.6",
    author="Pranav Singh",
    author_email="psingh2_be20@thapar.edu",
    description ="Evaluation of alternatives based on multiple criteria using TOPSIS method.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['Topsis_Pranav_102003432'],
    install_requires=['pandas'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "topsis=Topsis_Pranav_102003432.Pranav_102003432:main",
        ]
    } 
)