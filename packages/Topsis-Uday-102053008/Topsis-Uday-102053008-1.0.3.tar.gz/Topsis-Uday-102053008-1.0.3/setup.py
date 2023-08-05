from distutils.core import setup
setup(
  name = 'Topsis-Uday-102053008',         # How you named your package folder (MyLib)
  packages = ['Topsis-Uday-102053008'],   # Chose the same as "name"
  version = '1.0.3',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'The one stop tool to perform Multiple Criteria Decision Making(MCDM) using Topsis', 
  long_description="# TOPSIS-Uday-102053008 The package enables you to perform TOPSIS Multi Criteria Decision Making on the input csv file. The package outputs the csv file containing additional 2 columns, the TOPSIS SCORE and RANK assigned by the Topsis algorithm. ### How to INSTALL- pip install TOPSIS-Uday-102053008- TOPSIS-Uday-102053008 <InputDataFile> <Weights> <Impacts> <ResultFileName>- ✨Magic ✨ ### Example  - topsis '102053008-data.csv' '1,1,1,1,1' '+,-,+,+,+' '102053008-result.csv' ### Application - The algorithm could be used to rank different choices according to its impact and weight associated with each columns. The output is the rank of each choice with numerically lower rank is the preferred option and vice versa. ### License MIT [//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax) [dill]: <https://github.com/joemccann/dillinger> [git-repo-url]: <https://github.com/joemccann/dillinger.git>"
,  # Give a short description about your library
  author = 'Uday Uppal',                   # Type in your name
  author_email = 'uuppal_be20@thapar.edu',      # Type in your E-Mail
  url = 'https://github.com/uday-uppal',
  download_url='https://github.com/uday-uppal/Topsis-Uday-102053008/archive/refs/tags/1.0.3.tar.gz',
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
