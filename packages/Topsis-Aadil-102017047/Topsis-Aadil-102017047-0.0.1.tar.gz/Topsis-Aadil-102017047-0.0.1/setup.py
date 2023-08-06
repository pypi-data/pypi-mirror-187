import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="Topsis-Aadil-102017047",
    version="0.0.1",
    description="Useful in solving MCDM problems",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Aadil Singh",
    author_email="aadilsandhu7@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    packages=["topsis"],
    include_package_data=True,
    install_requires=['pandas'],
    entry_points={
        "console_scripts": [
            "topsis=topsis.__main__:main",
        ]
    },
)