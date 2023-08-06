from distutils.core import setup
setup(
  name = 'Topsis-Lagan-102003318',         # How you named your package folder (MyLib)
  packages = ['Topsis-Lagan-102003318'],   # Chose the same as "name"
  version = '1.0.4',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A package -> Calculates Topsis Score and Rank them accordingly',   # Give a short description about your library
  author = 'Lagan Garg',                   # Type in your name
  author_email = 'lgarg_be20@thapar.edu',      # Type in your E-Mail
  url = 'https://github.com/lagangarg/Topsis-Lagan-102003318',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/lagangarg/Topsis-Lagan-102003318/archive/refs/tags/1.0.4.tar.gz',    # I explain this later on
  
  install_requires=[            # I get to this in a second
          'numpy',
          'scrapeasy',
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