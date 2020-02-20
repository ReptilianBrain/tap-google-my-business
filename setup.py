import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tap-google-my-business",
    version="1.0.0",
    author="360 Agency",
    author_email="cgagnon@360.agency",
    description="Singer Tap for Google My Business A⁄PI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://360.agency",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.7'
)