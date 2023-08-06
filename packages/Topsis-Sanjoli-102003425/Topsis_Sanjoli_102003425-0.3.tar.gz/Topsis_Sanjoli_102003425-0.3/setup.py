from setuptools import setup 
with open("README.md", "r") as fh:
    long_description = fh.read()
setup(name="Topsis_Sanjoli_102003425",version="0.3",
description="This is a topsis package",
long_description=long_description,
    long_description_content_type="text/markdown",
author="Sanjoli Agarwal",
author_email="sagarwal_be20@thapar.edu",
packages=['Topsis_Sanjoli_102003425'],
install_requires=['pandas']
)



