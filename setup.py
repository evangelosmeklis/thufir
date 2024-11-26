from setuptools import setup, find_packages

setup(
    name="project_name",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # Add dependencies here
    ],
    entry_points={
        "console_scripts": [
            "thufir-cli=thufir.__main__:main",
        ],
    },
    author="Evangelos Meklis",
    description="A lightweight incident detection and resolution tool.",
    license="Apache License 2.0",
    python_requires=">=3.7",
)
