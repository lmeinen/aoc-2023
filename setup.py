from setuptools import find_packages
from setuptools import setup

setup(
    name="advent_of_code",
    version="1.0.0",
    url="https://github.com/lmeinen/aoc-2023",
    author="Lasse Meinen",
    license="WTFPL",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Games/Entertainment :: Puzzle Games",
    ],
    install_requires=[
        "advent-of-code-data >= 2.0.1",
    ],
    packages=find_packages(),
    entry_points={
        "adventofcode.user": ["github.lmeinen.1607830 = advent_of_code:solve"],
    },
)
