from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="Topsis_102003592_Bhavna",
    version="0.5",
    author="Bhavna Goyal",
    author_email="bgoyal_be20@thapar.edu",
    description ="Evaluation of alternatives based on multiple criteria using TOPSIS method.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['Topsis_102003592_Bhavna'],
    install_requires=['pandas'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "topsisbhav=Topsis_102003592_Bhavna.Bhavna_102003592:main",
        ]
    }
    
)