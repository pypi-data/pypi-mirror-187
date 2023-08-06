from  setuptools import setup,find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="Topsis-Vikas-102067010",
    version="1.0.8",
    author="Vikas Singh",
    author_email="vs8422135@gmail.com",
    description="Calculates Topsis Score and Rank them accordingly",
    long_description=long_description,
    keywords=['TOPSIS'],
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires='pandas',
    entry_points={
        "console_scripts": [
            "topsis=topsis.topsis:main"
        ]
    },
)