#
# This file is autogenerated during plugin quickstart and overwritten during
# plugin makedist. DO NOT CHANGE IT if you plan to use plugin makedist to update 
# the distribution.
#

from setuptools import setup, find_packages

kwargs = {'author': 'George Scott and Katherine Dykes',
 'author_email': 'systems.engineering@nrel.gov',
 'classifiers': ['Intended Audience :: Science/Research',
                 'Topic :: Scientific/Engineering'],
 'description': 'NREL Cost and Scaling Model',
 'download_url': '',
 'include_package_data': True,
 #'install_requires': ['openmdao.main'],
 #'keywords': ['openmdao'],
 'license': 'Apache v. 2.0',
 #'maintainer': '',
 #'maintainer_email': '',
 'name': 'NREL_CSM',
 'package_data': {'NREL_CSM': []},
 'package_dir': {'': 'src'},
 'packages': ['NREL_CSM'],
 #'url': '',
 'version': '0.1',
 'zip_safe': False}


setup(**kwargs)

