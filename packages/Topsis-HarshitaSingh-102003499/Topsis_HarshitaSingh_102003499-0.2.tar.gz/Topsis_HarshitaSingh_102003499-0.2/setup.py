from setuptools import setup 
with open("README.md", "r") as fh:
    long_description = fh.read()
setup(name="Topsis_HarshitaSingh_102003499",version="0.2",
description="This is a topsis code",
long_description=long_description,
    long_description_content_type="text/markdown",
# long_description="Technique for Order Preference by Similarity to Ideal Solution (TOPSIS) originated in the 1980s as a multi-criteria decision making method. TOPSIS chooses the alternative of shortest Euclidean distance from the ideal solution, and greatest distance from the negative-ideal solution.",
author="Harshita",
packages=['Topsis_HarshitaSingh_102003499'],
install_requires=['pandas']
)