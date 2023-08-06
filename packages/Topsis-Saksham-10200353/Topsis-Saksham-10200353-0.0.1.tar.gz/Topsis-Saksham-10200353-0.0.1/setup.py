
# import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

# setuptools.setup(
#     name="Topsis-Saksham-102003533",
#     version="1.0.0",
#     author="Saksham Yadav",
#     # group="",
#     author_email="syadav1_be20@thapar.edu",
#     description="A package -> Calculates Topsis Score and Ranks them accordingly",
#     long_description=long_description,
#     long_description_content_type="text/markdown",
#     license="MIT",
#     # url="https://github.com/Tewatia5355/Topsis_tewatia",
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: OS Independent",
#     ],
#     packages=["Topsis-Saksham-102003533"],
#     include_package_data=True,
#     install_requires=['pandas', 'numpy', 'os', 'sys'],
#     entry_points={
#         "console_scripts": [
#             "topsis=Topsis-Saksham-102003533.__init__:main",
#         ]
#     },
# )

from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'A package -> Calculates Topsis Score and Ranks them accordingly'
LONG_DESCRIPTION = 'A package that allows to build simple streams of video, audio and camera data.'

# Setting up
setup(
    name="Topsis-Saksham-10200353",
    version=VERSION,
    author="Saksham Yadav",
    author_email="syadav1_be20@thapar.edu",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pandas', 'numpy', 'os', 'sys'],
    keywords=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)