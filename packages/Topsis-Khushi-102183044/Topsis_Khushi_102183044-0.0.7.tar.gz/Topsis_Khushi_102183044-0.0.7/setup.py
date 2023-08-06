import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Topsis_Khushi_102183044",
    version="0.0.7",
    author="Khushi Prasad",
    author_email="khushipr01@gmail.com",
    description="Package for calculating topsis score for multiple criteria decision making problems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/khushipr/TOPSIS",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["Topsis_Khushi_102183044"],
    include_package_data=True,
    install_requires='pandas',
    entry_points={
        "console_scripts": [
            "topsis=Topsis_Khushi_102183044.topsis:main",
        ]
    },
)