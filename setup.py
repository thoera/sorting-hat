from setuptools import find_packages, setup

setup(
    name="sorting-hat",
    version="1.0.0",
    description="Find out what will be your real house by using the sorting hat!",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Click",
        "pandas",
        "questionary",
    ],
    entry_points={
        "console_scripts": [
            "sorting-hat = cli:cli",
        ],
    },
)
