# from distutils.core import setup
from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
  name = 'Topsis_Keshav_Garg_102017064',         # How you named your package folder (MyLib)
  packages = ['Topsis_Keshav_Garg_102017064'],   # Chose the same as "name"
  version = '0.0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This package performs the topsis(multiple criterion decision making) on a pandas dataframe and return the rank and topsis score.',   # Give a short description about your library
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Keshav Garg',                   # Type in your name
  author_email = 'gkeshav2309@gmail.com',# Type in your E-Mail
  url = 'https://github.com/keshavgarg23/Topsis-Keshav-102017064',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/keshavgarg23/Topsis-Keshav-102017064/archive/refs/tags/v.0.0.1.tar.gz',    # I explain this later on
  keywords = ['TOPSIS', 'MCDM', 'DECISION','MAKING'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',
          'pandas',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)