from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="noteerr",
    version="1.1.0",
    author="Naufal",
    description="A CLI tool to log, annotate, and recall command errors",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/naufalkmd/Noteerr",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "colorama>=0.4.4",
        "rich>=10.0.0",
    ],
    entry_points={
        "console_scripts": [
            "noteerr=noteerr.cli:main",
        ],
    },
)
