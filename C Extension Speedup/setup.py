# setup.py
from setuptools import setup, Extension

setup(
    name="fast_factorial_repetition",
    version="0.1",
    ext_modules=[
        Extension("fast_factorial_repetition", ["fast_factorial_repetition.c"])
    ]
)

