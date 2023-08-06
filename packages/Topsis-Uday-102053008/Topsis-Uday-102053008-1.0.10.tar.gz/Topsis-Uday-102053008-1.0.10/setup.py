from setuptools import setup, find_packages
setup(
  name = 'Topsis-Uday-102053008',         # How you named your package folder (MyLib)
  version = '1.0.10',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  packages = find_packages(),
        entry_points ={
            'console_scripts': [
                'Topsis-Uday-102053008 = topsisfolder.topsisModule:topsis'
            ],
        },
  description = 'The one stop tool to perform Multiple Criteria Decision Making(MCDM) using Topsis', 
  long_description="# TOPSIS-Uday-102053008 \n \
  The package enables you to perform TOPSIS Multi Criteria Decision Making on the input csv file. The package outputs the csv file containing additional 2 columns, the TOPSIS SCORE and RANK assigned by the Topsis algorithm.  \n \
  ### How to INSTALL  \n \
  - pip install TOPSIS-Uday-102053008  \n \
  - Topsis-Uday-102053008 <InputDataFile> <Weights> <Impacts> <ResultFileName>  \n \
  - ✨Magic ✨ ### Example  - Topsis-Uday-102053008 '102053008-data.csv' '1,1,1,1,1' '+,-,+,+,+' '102053008-result.csv'  \n \
   ### Application  \n \
   - The algorithm could be used to rank different choices according to its impact and weight associated with each columns. The output is the rank of each choice with numerically lower rank is the preferred option and vice versa.  \n \
  ### License  \n\
  ###  MIT"
,  # Give a short description about your library
  author = 'Uday Uppal',                   # Type in your name
  author_email = 'uuppal_be20@thapar.edu',      # Type in your E-Mail
  url = 'https://github.com/uday-uppal',
  long_description_content_type ="text/markdown",
  keywords = ['TOPSIS', 'MACHINE LEARNING', 'STATISTICS'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',
          'pandas',
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)