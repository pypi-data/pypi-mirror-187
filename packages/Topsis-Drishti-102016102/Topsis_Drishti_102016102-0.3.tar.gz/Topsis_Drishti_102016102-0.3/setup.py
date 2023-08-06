
from distutils.core import setup
setup(
  name = 'Topsis_Drishti_102016102',         # How you named your package folder (MyLib)
  packages = ['Topsis_Drishti_102016102'],   # Chose the same as "name"
  version = '0.3',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'topsis',   # Give a short description about your library
  author = 'Drishti bhatia',                   # Type in your name
  author_email = 'drishtibhatia2020@gmail.com',      # Type in your E-Mail
      # I explain this later on
  long_description='''Project description
TOPSIS
Technique for Order Preference by Similarity to Ideal Solution (TOPSIS)
Technique for Order Preference by Similarity to Ideal Solution (TOPSIS) came in the 1980s as a multi-criteria-based decision-making method. TOPSIS chooses the alternative of shortest the Euclidean distance from the ideal solution and greatest distance from the negative ideal solution.

TOPSIS is a way to allocate the ranks on basis of the weights and impact of the given factors:.

Weights mean how much a given factor should be taken into consideration
Impact means that a given factor has a positive or negative impact.
This tool allows you to calculate the topsis ranking and save the results in the form of a csv (Comma Seperated Value) file.

Installing Package
pip install Topsis-Drishti-102016102
Using the TOPSIS tool
Create a script by importing the package and just calling the TOPSIS function.
import importlib
topsis=importlib.import_module("Topsis_Drishti_1016102")
topsis.TOPSIS()
Run the Script through command line as shown below:
C:/Users/admin> python myscript.py <Data_File_csv> <Weights(Comma_seperated)> <Impacts(Comma_seperated)> <Result_file_csv>
''',
  long_description_content_type='text/markdown',
  keywords = ['topsis'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas',
          'numpy',
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
