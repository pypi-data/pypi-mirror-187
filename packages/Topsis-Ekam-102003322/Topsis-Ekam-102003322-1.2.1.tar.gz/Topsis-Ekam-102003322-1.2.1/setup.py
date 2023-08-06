from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
  name = 'Topsis-Ekam-102003322',         # How you named your package folder (MyLib)
  packages = ['Topsis-Ekam-102003322'],   # Chose the same as "name"
  version = '1.2.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://github.com/Ekam3000/Python-Package-TOPSIS/blob/main/LICENSE
  
  description = 'This package is implimentation of multi-criteria decision analysis using topsis',   # Give a short description about your library
  long_description = readme(),
  long_description_content_type ="text/markdown",
  author = 'Ekam',                   # Type in your name
  author_email = 'ekambhelle030@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/Ekam3000/Python-Package-TOPSIS',   # Provide either the link to your github or to your website
  # url of the package page in  Python Package Index (PyPI) 
  keywords = ['topsis'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',
          'pandas',
          ''
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
  python_requires='>=3.6',
)




