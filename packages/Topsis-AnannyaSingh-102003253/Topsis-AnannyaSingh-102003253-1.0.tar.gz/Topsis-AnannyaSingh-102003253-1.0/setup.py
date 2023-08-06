from setuptools import setup, find_packages

setup(
    name='Topsis-AnannyaSingh-102003253',
    version='1.0',
    description='Python implementation of the Technique for Order of Preference by Similarity to Ideal Solution (TOPSIS)',
    author='Anannya Singh',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas'
    ],
)