import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Topsis-Romil-102003290", 
    version="1.0.4",
    author="Romil Gupta",
    author_email="rgupta2_be20@thapar.edu",
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
            "topsis=topsis._main_:main"
        ]
    },
    python_requires='>=3.6',
    
)