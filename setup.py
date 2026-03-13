# Fallback for pip install -e when pyproject.toml package discovery fails
from setuptools import setup, find_packages

setup(
    name="supportdesk",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
)
