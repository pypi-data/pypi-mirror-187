from setuptools import setup, find_packages

with open("README.md", "r") as fh:
  LONG_DESCRIPTION = fh.read()

setup(
  name = 'Topsis-Abhinav-102067004',           
  version = '0.1.1',
  author = 'Abhinav Tyagi',                   
  author_email = 'atyagi_be20@thapar.edu',
  description = 'Implementation of topsis algorithm for multiple criteria decision making',             
  long_description=LONG_DESCRIPTION,
  long_description_content_type="text/markdown",      
  url = 'https://github.com/tyagi-abhinavv',  
  packages = find_packages(),
  install_requires=['numpy', 'pandas', 'pathlib'],
  entry_points={
    'console_scripts': [
        'topsis= topsis.topsis:main',
    ],
  } ,
  classifiers=[

    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ],
  python_requires='>=3.6',
)