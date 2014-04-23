from setuptools import setup, find_packages

setup(
    name="py-handleclient",
    version="0.6",
    packages=find_packages(),
    install_requires=[
        'requests >= 2.0'
    ],
    author="Matt Cordial",
    author_email="matt.cordial@asu.edu",
    description=(
        "A client which communicates with the Handle Administration "
        "Web Service."
    ),
    keywords="cnri handle server web-service",
)
