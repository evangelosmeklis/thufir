from setuptools import setup, find_packages

setup(
    name="thufir",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "thufir=thufir.cli:cli",
        ],
    },
    author="Evangelos Meklis",
    description="A lightweight incident detection and resolution tool.",
    license="Apache License 2.0",
    python_requires=">=3.7",
)