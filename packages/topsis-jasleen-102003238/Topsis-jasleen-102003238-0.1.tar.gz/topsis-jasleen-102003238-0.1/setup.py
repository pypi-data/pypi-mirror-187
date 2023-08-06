import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="topsis-jasleen-102003238",
    version="0.1",
    author="jasleen phutela",
    author_email="jphutela_be20@thapar.edu",
    description="mplements topsis on the given input data file and generates topsis score and ranks accordingly.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
