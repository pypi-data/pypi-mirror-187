
from setuptools import setup
with open("readme.txt", "r") as fh:
    long_description = fh.read()


setup(name="topsis_102003451",
version ="0.1",
description ="This is package for topsis of version 0.3",
long_description=long_description,
     long_description_content_type="text/markdown",
author="Riya",
author_email="rriya_be20@thapar.edu",
packages=['topsis_102003451'],
install_requires=['pandas'],
include_package_data=True,
    entry_points={
            "console_scripts": [
                "topsis123=topsis_102003451.topsis:main",
            ]
    }
)

