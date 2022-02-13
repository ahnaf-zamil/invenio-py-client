from setuptools import setup

from invenio_client import _about

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requirements = fh.read().split("\n")


setup(
    name="invenio-py-client",
    author=_about.__author__,
    author_email=_about.__email__,
    version=_about.__version__,
    description=_about.__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    license=_about.__license__,
    url=_about.__github__,
    packages=["invenio_client", "invenio_client.client"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
    ],
    python_requires=">=3.6",
    include_package_data=True,
    exclude=("__pycache__",),
    install_requires=requirements,
)