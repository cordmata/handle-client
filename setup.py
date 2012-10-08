from setuptools import setup, find_packages

setup(
    name = "py-handleclient",
    version = "0.5",
    packages = find_packages(),
    install_requires = [
        'requests >= 0.14'
    ],
    author = "Matt Cordial",
    author_email = "matt.cordial@asu.edu",
    description = "A client which communicates with the Handle Administration Web Service.",
    keywords = "cnri handle server web-service",
)
