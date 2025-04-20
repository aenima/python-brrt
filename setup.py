#!/usr/bin/env python

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="brrt",
    version="0.1",
    description="Dot matrix printer interface",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="alxasfuck",
    url="https://github.com/alxasfuck/python-brrt",
    packages=["brrt"],
    package_data={"": ["LICENSE"]},
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.12",
    install_requires=["PyYAML"],
    license="GPL",
    zip_safe=False,
    tests_require=["pytest", "pytest-cov"],
)
