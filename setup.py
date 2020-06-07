import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pydustry",
    version="0.0.4",
    author="Ado1928",
    author_email="ado.gamer123@gmail.com",
    description="A package for getting Mindustry server status and sending commands.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ado1928/pydustry/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    py_modules=["pydustry"],
)