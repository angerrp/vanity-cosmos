from os import path

import setuptools


def read(file_name: str) -> str:
    """Helper to read README."""
    this_directory = path.abspath(path.dirname(__file__))
    with open(path.join(this_directory, file_name), encoding="utf-8") as f:
        return f.read()


setuptools.setup(
    name="etimoz",
    version="0.1.0",
    author="Paul Angerer",
    author_email="etimoz@users.noreply.github.com",
    description="Tool for generating custom cosmos addresses.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/etimoz/vanity-cosmos/",
    keywords="cosmos blockchain atom cryptocurrency address generator vanity",
    zip_safe=False,
    packages=setuptools.find_packages(),
    classifiers=[],
    python_requires=">=3.6",
    install_requires=["bech32", "secp256k1",],
)
