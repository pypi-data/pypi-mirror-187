import sys
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from codecs import open

if sys.version_info[:3] < (3, 0, 0):
    print("Requires Python 3 to run.")
    sys.exit(1)

with open("README.md", encoding="utf-8") as file:
    readme = file.read()

setup(
    name="pickle_wrap",
    description="Wraps pickles",
    long_description=readme,
    long_description_content_type="text/markdown",
    version="v0.0.0",
    packages=["pickle_wrap"],
    python_requires=">=3",
    url="https://github.com/paulcbogdan/pickle_wrap",
    author="paulcbogdan",
    author_email="paulcbogdan@gmail.com",
    # classifiers=[],
    install_requires=[],
    keywords=["pickling", "wrapping"],
    license="MIT"
)