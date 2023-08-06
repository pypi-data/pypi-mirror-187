from setuptools import setup, find_packages

setup(
   name='mypckg1',
   version='0.0.0',
   description='A useful module',
   author='Mb',
   author_email='mad@ab.work',
   #packages=['mypckg1'],  #same as name
   install_requires=[],
   packages=find_packages('mypckg1'),

   )
