# setup.py
from setuptools import setup #, find_packages

setup(
    name='nrel_csm',
    version='0.1',
    description='NREL cost and scaling model',
    author='G. Scott and K. Dykes',
    author_email='systems.engineering@nrel.gov',
    #packages= find_packages(),
    packages=['nrelcsm', 'nrelcsm.static'],
    package_data={'':['*.txt']},
    include_package_data = True,
    package_dir={'': 'src'},
    license='Apache License, Version 2.0',
)