import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="topsis_aaryan_102003541", 
    version="1.0.0",
    author="Aaryan Jain",
    author_email="jainaaryan2001@gmail.com",
    description="topsis implementation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "aaryan=aaryan.__main__:main"
        ]
    },
    python_requires='>=3.6',
)