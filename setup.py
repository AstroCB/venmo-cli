from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()


setup(
    name="venmo",
    version="0.1.0",
    author="Cameron Bernhardt",
    author_email="me@cameronbernhardt.com",
    license_files=["LICENSE.md"],
    description="A simple CLI for Venmo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AstroCB/venmo-cli",
    py_modules=["venmo"],
    install_requires=[requirements],
    entry_points={
        "console_scripts": [
            "venmo = venmo:cli",
        ],
    },
)
