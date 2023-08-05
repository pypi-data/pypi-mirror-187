# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 18:18:45 2023

@author: jeetb
"""

from setuptools import setup, find_packages

setup(
  name = 'TOPSIS-Samarjeet-102183052',         # How you named your package folder (MyLib)
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = "Topsis Value Calculator- 'TOPSIS-Samarjeet-102183052' is a Python package implementing Multi-criteria decision making (MCDM) using Topsis. Topsis stands for Technique for Order of Preference by Similarity to Ideal Solution. Just provide your input attributes and it will give you the results ",   # Give a short description about your library
  author = 'Samarjeet Baliyan',                   # Type in your name
  author_email = 'jeetbaliyan.2002@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/Samar3007',   # Provide either the link to your github or to your website
  keywords = ['topsis', 'Samarjeet', '102183052'],   # Keywords that define your package best
  packages = find_packages(),   
  include_package_data = True,
  install_requires=[
          'pandas',
          'tabulate'
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',       
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3'
  ]    
)