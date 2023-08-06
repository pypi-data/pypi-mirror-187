
from distutils.core import setup
setup(
  name = 'Topsis_AVIRAL_102016049',         # How you named your package folder (MyLib)
  packages = ['Topsis_AVIRAL_102016049'],   # Chose the same as "name"
  version = '1.0.3',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  long_description = '''# Topsis implementation for Multiple Criteria Decision Making (MCDM)

Topsis-AVIRAL-102016049 is a Python Package that can be used as CLI tool to calculate TOPSIS performance score and ranking them according to score by taking csv file as input.

## What is TOPSIS?
**T**echnique for **O**rder **P**reference by **S**imilarity to **I**deal **S**olution (TOPSIS) originated in the 1980s as a multi-criteria decision making method. TOPSIS chooses the alternative of shortest Euclidean distance from the ideal solution, and greatest distance from the negative-ideal solution.

## Installation

Install the package using command-
 sh
pip install Topsis-AVIRAL-102016049


## How to use this package?

- ### To use via CLI
   sh
  topsis input_file weights impacts output_file
  
  ##### Arguments
  ####
  | Arguments | Description |
  | ------ | ------ |
  | input_file | Input CSV file path |
  | weights | Comma seperated numbers enclosed in "" |
  | impacts | Comma seperated '+' or '-' enclosed in "" |
  | output_file | Output CSV file path |
  
  ##### Output:
  Creates a ouput_file that contains the original data with two new columns as performance score and rank.
  
  Example:
  sh
  topsis input_data.csv "1,1,1,2,1" "+,+,+,-,+" output_file.csv
  
  #
 - ### To use in .py script
   #
   python
   <br>
   import Topsis_AVIRAL_102016049 as topsis

   import pandas as pd
   
   dataset = pd.read_csv("data.csv")
   data = dataset[:,1:]
   weights = [1,1,1,2,1]
   impacts = ["+","+","+","-","+"]
   topsisscore(data,weights,impacts,output.csv)
   
   
   ### Sample Input CSV
   #
   | Fund Name | P1 | P2 | P3 | P4 | P5 |
   | ------ | ------ | ------ |------ |------ |------ |
   | M1 | 0.65 | 0.42 | 4.2 | 60.1 | 16.34 |
   | M2 | 0.67 | 0.45 | 6.8 | 69.7 | 19.41 |
   | M3 | 0.91 | 0.83 | 6.5 | 62.9 | 17.79 |
   | M4 | 0.61 | 0.37 | 3.3 | 44.1 | 12.1 |
   | M5 | 0.8 | 0.64 | 5.5 | 55.4 | 15.59 |
   | M6 | 0.79 | 0.62 | 5.5 | 56.5 | 15.85 |
   | M7 | 0.82 | 0.67 | 5.1 | 53.6 | 15.05 |
   | M8 | 0.94 | 0.88 | 5.1 | 44.5 | 12.86 |
   
   ### Sample Output CSV File
   ### For weights "1,1,1,1,1" and impacts "+,-,+,-,+"
   #
   | Fund Name | P1 | P2 | P3 | P4 | P5 | Topsis Score | Rank |
   | ------ | ------ | ------ |------ |------ |------ | ------ | ------ |
   | M1 | 0.65 | 0.42 | 4.2 | 60.1 | 16.34 | 0.53475795 | 3 |
   | M2 | 0.67 | 0.45 | 6.8 | 69.7 | 19.41 | 0.64308057 | 1 |
   | M3 | 0.91 | 0.83 | 6.5 | 62.9 | 17.79 | 0.50063048 | 6 |
   | M4 | 0.61 | 0.37 | 3.3 | 44.1 | 12.1 | 0.50478334 | 5 |
   | M5 | 0.8 | 0.64 | 5.5 | 55.4 | 15.59 | 0.53326848 | 4 |
   | M6 | 0.79 | 0.62 | 5.5 | 56.5 | 15.85 | 0.5446234 | 2 |
   | M7 | 0.82 | 0.67 | 5.1 | 53.6 | 15.05 | 0.48796329 | 7 |
   | M8 | 0.94 | 0.88 | 5.1 | 44.5 | 12.86 | 0.4227203 | 8 |
   ''',
   long_description_content_type='text/markdown',
  description = 'Topsis',   # Give a short description about your library
  author = 'AVIRAL JAIN',                   # Type in your name
  author_email = 'ajain4_be20@thapar.edu',      # Type in your E-Mail
  
  keywords = ['topsis'],   # Keywords that define your package best
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
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.11',
  ],
)