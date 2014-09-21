# setup.py
from setuptools import setup, find_packages

kwargs = {'author': 'George Scott and Katherine Dykes',
 'author_email': 'systems.engineering@nrel.gov',
 'include_package_data': True,
 'license': 'Apache License v 2.0',
 'name': 'nrel_csm',
 'package_data': {'nrel_csm': ['*.txt'], 'nrel_csm': ['static/*.txt'], 'nrel_csm.static': ['*.txt']},
 'package_dir': {'': 'src'},
 'packages': ['nrel_csm', 'nrel_csm.static'],
 'version': '0.1',
 'zip_safe': False}


setup(**kwargs)

