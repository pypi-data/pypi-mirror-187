from setuptools import setup 
with open("README.md", "r") as fh:
    long_description = fh.read()
setup(name="Topsis_Harshita_Saxena_102003497",version="0.4",
description="Given package has the code for topsis, which is one of the techniques used for multiple criteria decision making. It chooses the Euclidean distance from the ideal solution and greatest distance from the negative ideal solution. ",
long_description=long_description,
    long_description_content_type="text/markdown",
# long_description="Technique for Order Preference by Similarity to Ideal Solution (TOPSIS) originated in the 1980s as a multi-criteria decision making method. TOPSIS chooses the alternative of shortest Euclidean distance from the ideal solution, and greatest distance from the negative-ideal solution.",
author="Harshita Saxena",
packages=['Topsis_Harshita_Saxena_102003497'],

install_requires=['pandas'],
entry_points={
        "console_scripts": [
            "topsis=Topsis_Harshita_Saxena_102003497.topsis:main",
        ]
    },
)