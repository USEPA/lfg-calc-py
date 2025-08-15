"""
Setup for landfill package
"""

from setuptools import setup, find_packages

setup(
    name='lfg-calc-py',
    version='0.1.0',
    packages=find_packages(),
    package_dir={'lfg-calc-py': 'lfg-calc-py'},
    include_package_data=True,
    python_requires=">=3.11",
    install_requires=[
        'StEWI @ git+https://github.com/USEPA/standardizedinventories.git#egg=StEWI',
        'numpy>=2.2.4',
        'pandas>=2.2.3',
        'pip>=23.2.1',
        'pyyaml>=6.0.2',
        'sympy>=1.13.3',
        'pathlib>=1.0.1'
    ],
    url='https://github.com/USEPA/FLOWSA',
    license='MIT',
    author='Katherine Latoff, Catherine Birney, Max Krause, and P. Ozge Kaplan',
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
