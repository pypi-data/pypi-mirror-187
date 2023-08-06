from setuptools import setup, find_packages

setup(
   setup_requires=['wheel'],
   name='mypckg1',
   version='0.0.1',
   description='A useful module',
   author='Mb',
   #package_dir={'':'mypckg1'},
   author_email='mad@ab.work',
   packages=['mypckg1'],  #same as name
   install_requires=[],
   #packages=find_packages('mypckg1'),

   )
