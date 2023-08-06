from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  #'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='102053024',
  version='0.0.1',
  description='Topsis Code',
  long_description=open('readme.txt').read() + '\n\n' + open('changelog.txt').read(),
  url='',  
  author='Khushi Bathla',
  author_email='kbathla_be20@thapar.edu',
  #license='MIT', 
  classifiers=classifiers,
  keywords='topsis', 
  packages=find_packages(),
  install_requires=[''] 
)
