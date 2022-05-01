from importlib.metadata import entry_points
from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as doc_file:
    long_description = doc_file.read()

setup(
    name="jsondiffer",
    version="1.0.0",
    description="A diffing tool for comparing json files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Osamudiamen Emmanuel Azamegbe",
    author_email="osas.azamegbe@gmail.com",
    url="https://github.com/OsasAzamegbe/jsondiffer",
    license="MIT",
    packages=find_packages(exclude=["tests"]),
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Operating System :: POSIX :: Linux",
    ],
    entry_points={"console_scripts": ["jsdiff=jsondiffer.main:main"]},
    keywords=["json", "differ", "difftool", "diff", "json diff", "diffing"],
    python_requires=">=3.10",
)
