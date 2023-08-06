
from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="topsis-raunak-102017148",
    version="1.0.0",
    description="A Python package to get optimal solutiion.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Raunak Kumar",
    author_email="raunakkumar071201@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["topsis"],
    include_package_data=True,
    install_requires=["pandas","numpy"],
    entry_points={
        "console_scripts": [
            "topsis=topsis.102017148:main",
        ]
    },
)