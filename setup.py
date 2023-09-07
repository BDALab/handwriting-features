import pathlib
from setuptools import setup, find_packages


# Get the long description from the README file
long_description = (pathlib.Path(__file__).parent.resolve() / "README.md").read_text(encoding="utf-8")

# Prepare the packages and requirements
packages = find_packages(where="src")
requires = [
    "numpy",
    "pandas",
    "scipy",
    "handwriting-sample",
]

# Prepare the setup
setup(
    name="handwriting-features",
    version="1.0.8",
    description="Handwriting features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BDALab/handwriting-features",
    author="Brain Diseases Analysis Laboratory",
    author_email="galaz@vut.cz",
    packages=packages,
    package_data={"": ["LICENSE"]},
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=requires,
    python_requires=">=3.7",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent"
    ]
)
