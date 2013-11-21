#

from setuptools import setup, find_packages

setup(
 name='NREL_CSM',
 version='0.1',
 author='George Scott and Katherine Dykes',
 author_email='systems.engineering@nrel.gov',
 #url='',
 classifiers = ['Intended Audience :: Science/Research',
                 'Topic :: Scientific/Engineering'],
 description='NREL Cost and Scaling Model',
 #download_url= '',
 license='Apache v. 2.0',

 # adding packages
 packages= ['NREL_CSM', 'NREL_CSM.static'],
 package_dir = {'':'src'},

 # trying to add files...
 include_package_data = True,
 package_data = {
      '': ['*.txt'],
      '': ['static/*.txt'],
      'static': ['*.txt'],
  },

 zip_safe=False,
 install_requires=['distribute'],
)