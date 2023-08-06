from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="Topsis_Aditya_102003424",
    version="0.2",
    author="Aditya Singh Rathore",
    author_email="arathore_be20@thapar.edu",
    description ="Evaluation of alternatives based on multiple criteria using TOPSIS method",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['Topsis_Aditya_102003424'],
    install_requires=['pandas'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "topsis=Topsis_Aditya_102003424.Aditya_102003424:main",
        ]
    } 
)