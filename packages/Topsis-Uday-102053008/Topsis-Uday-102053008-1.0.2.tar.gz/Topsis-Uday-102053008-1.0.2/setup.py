from distutils.core import setup
setup(
  name = 'Topsis-Uday-102053008',         # How you named your package folder (MyLib)
  packages = ['Topsis-Uday-102053008'],   # Chose the same as "name"
  version = '1.0.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'The one stop tool to perform Multiple Criteria Decision Making(MCDM) using Topsis', 
  long_description="long desc",  # Give a short description about your library
  author = 'Uday Uppal',                   # Type in your name
  author_email = 'uuppal_be20@thapar.edu',      # Type in your E-Mail
  url = 'https://github.com/uday-uppal',
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
