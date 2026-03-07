from setuptools import setup, find_packages

setup(
    name="racing-demo",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "arcade>=2.7.0",
        "pytest>=7.4.0",
        "pyinstaller>=6.0.0",
        "numpy>=1.24.0",
    ],
)
