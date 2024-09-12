from setuptools import setup, find_packages

setup(
    name="watsonx_connector",
    # version="{{VERSION_VAR}}",
    version="0.0.1",
    description="IBM Watsonx API wrapper package for calling text generation and embedding requests",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jackpots28/watsonx_connector",
    author="Jack Sims",
    author_email="jack.m.sims@protonmail.com",
    license="GPL",
    packages=find_packages(include=['WatsonxConnector', 'WatsonxConnector.*']),
    install_requires=[
        "setuptools",
        "wheel",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: POSIX :: Linux",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3.11",
    ],
)
