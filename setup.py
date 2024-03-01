from setuptools import setup, find_packages
import os

def main():
    setup(
        name='ptins',
        version='0.0.1',
        description="debug tool for pytorch model",
        author="MayDomine",
        author_email="why1.2seed@gmail.com",
        packages=find_packages(),
        url="https://github.com/MayDomine/ptins",
        install_requires=[
            "torch",
        ],
        keywords="pytorch, debug, inspect, hook",
        license='Apache 2.0',
    )

if __name__ == '__main__':
    main()