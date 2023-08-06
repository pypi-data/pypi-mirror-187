# It configures all your package’s contents and all sorts of auxiliary information.
# You can then create a distribution of your package using the following command:
# python setup.py sdist
# This will create a dist directory containing a distribution archive file in the .tar.gz format.
# You can then install your package using pip install:
# pip install /path/to/my_package-0.1.tar.gz

from setuptools import setup

with open("README.md") as file:
    long_description = file.read()

setup(
    name="robin_sd_upload",
    packages=["robin_sd_upload"],
    install_requires=["validators>=0.18.2", "PyYAML>=5.4.1", "requests>=2.25.1", "zipfile36>=0.1.3", "nano>=0.1.0"],
    entry_points={
    'console_scripts': [
        'robin_sd_upload = robin_sd_upload.__main__:main',
    ],
    },
    version="0.1.16",
    license="MIT",
    description="Package to upload files to the Robin Radar API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Robin Radar Systems",
    author_email="tivadar.kamondy@robinradar.com",
    url="https://bitbucket.org/robin-radar-systems/sd-api-upload-pip-package.git",
    keywords=["python", "robin", "radar", "download", "software", "sd"]
)
