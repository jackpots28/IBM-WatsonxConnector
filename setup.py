import setuptools
from setuptools import setup

setup(
    name="WatsonxConnector",
    version="{{VERSION_VAR}}",
    # version="0.0.1",
    description="IBM Watsonx API wrapper package for calling text generation and embedding requests",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jackpots28/watsonx_connector",
    author="Jack Sims",
    author_email="jack.m.sims@protonmail.com",
    license="Apache-2.0",
    packages=setuptools.find_packages(exclude=("examples",)),
    install_requires=[
        "setuptools",
        "wheel",
        "requests",
        "urllib3~=2.2.3"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12"
    ],
)

