from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
   long_description = fh.read()

setup(
    name="Topsis-Anshu-102003618",
    version="1.0.0",
    author="Anshu Misra",
    author_email="anshumisra.25@gmail.com",
    description="Calculating topsis score and finding rank",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/anshumisra/Topsis-Anshu-102003618",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={'':'src'},
    py_modules=['Topsis-Anshu-102003618'],
    include_package_data=True,
    install_requires=['pandas','numpy','os','sys','requests'],
    
)