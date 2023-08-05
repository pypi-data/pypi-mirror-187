from distutils.core import setup

setup(
  name = 'Topsis-Abhinav-102067004',         # How you named your package folder (MyLib)
  packages = ['Topsis-Abhinav-102067004'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Implementation of topsis algorithm for multiple criteria decision making',   # Give a short description about your library
  author = 'Abhinav Tyagi',                   # Type in your name
  author_email = 'atyagi_be20@thapar.edu',      # Type in your E-Mail
  url = 'https://github.com/tyagi-abhinavv',
  keywords = ['Topsis', 'MCDM'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',
          'pandas',
          'pathlib',
      ],
  entry_points={
    'console_scripts': [
        'topsis= Topsis-Abhinav-102067004.topsis:main',
    ],
  } ,
  classifiers=[

    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ],
)