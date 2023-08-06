from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = []

setup(
    name="datret",
    version="1.0.0",
    author="Timur Abdualimov",
    author_email="timur.atp@yandex.ru",
    description="Tensorflow implementation for structured tabular data",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/AbdualimovTP/datret",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
    ],
)
