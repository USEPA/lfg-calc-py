"""
Setup for lfg-calc-py package
"""

from setuptools import setup

setup(
    name='lfg_calc_py',
    version='0.0.1',
    packages=['lfg-calc-py'],
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=[
        'numpy',
        'pandas',
        'pip',
        'pyyaml',
        'sympy',
        'pathlib'
    ],
    url='https://github.com/USEPA/lfg-calc-py',
    license='MIT',
    author='Katherine Latoff, Catherine Birney, Andrew Beck, Max Krause, and Wesley '
           'Ingwersen',
    author_email='ingwersen.wesley@epa.gov',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: IDE",
        "Intended Audience :: Science/Research",
        "License :: MIT",
        "Programming Language :: Python :: 3.x",
        "Topic :: Utilities",
    ],
    description='Landfill emission model.'
)
