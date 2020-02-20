import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mp3-tools-carsten-engelke", # Replace with your own username
    version="1.0.0",
    author="Carsten Engelke",
    author_email="carsten.engelke@gmail.com",
    description="Tools for merging mp3 files using foobar2000, e.g. audiobooks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/carsten-engelke/mp3-tools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)