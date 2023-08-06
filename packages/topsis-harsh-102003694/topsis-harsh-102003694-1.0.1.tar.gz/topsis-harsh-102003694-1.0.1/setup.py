import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="topsis-harsh-102003694",
    version="1.0.1",
    author="Harsh Bisla",
    author_email="harshbisla10102001@gmail.com",
    description="topsis implementation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
