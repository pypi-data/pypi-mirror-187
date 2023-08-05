import setuptools
from setuptools import setup, find_packages
#from gister.version import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
# packages = ["gister"],
# url="https://github.com/pypa/sampleproject",
#project_urls={
#    "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
#},
setuptools.setup(
    name="gister-cli",
    version="0.0.4",
    author="Josh Andres",
    author_email="josh.an.bas@gmail.com",
    description="A awesome cli project.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={'': "gister"},
    packages=find_packages("gister"),
    python_requires=">=3.6",
    install_requires=[
        'requests',
        'ruamel.yaml==0.17.17',
        'importlib; python_version == "3.6"',
    ],
    entry_points={
        'console_scripts': [
            'gister=gister.cli:main'
        ],
    },
)
