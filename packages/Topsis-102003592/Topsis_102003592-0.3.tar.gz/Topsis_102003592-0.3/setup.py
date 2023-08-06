from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="Topsis_102003592",
    version="0.3",
    author="Bhavna Goyal",
    author_email="bgoyal_be20@thapar.edu",
    description ="Evaluation of alternatives based on multiple criteria using TOPSIS method.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['Topsis_102003592'],
    install_requires=['pandas']
    
)