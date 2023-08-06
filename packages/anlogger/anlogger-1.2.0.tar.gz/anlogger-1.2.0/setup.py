import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="anlogger",
  version="1.2.0",
  author="anttin",
  author_email="muut.py@antion.fi",
  description="Module to assist in setting up logging.",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/anttin/anlogger",
  packages=setuptools.find_packages(),
  classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
  ]
)
