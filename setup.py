"""
Setup for landfill package
"""

from setuptools import setup, find_packages

setup(
    name='landfill',
    version='0.0.1',
    packages=find_packages(),
    package_dir={'landfill': 'landfill'},
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
