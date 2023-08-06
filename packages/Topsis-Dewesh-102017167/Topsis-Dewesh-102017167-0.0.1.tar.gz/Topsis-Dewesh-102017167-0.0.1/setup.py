from distutils.core import setup
with open("README.md","r") as d:
    desc = d.read()
setup(
  name = 'Topsis-Dewesh-102017167',         # How you named your package folder (MyLib)
  packages = ['Topsis-Dewesh-102017167'],   # Chose the same as "name"
  version = '0.0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = desc,   # Give a short description about your library
  author = 'Dewesh Agrawal',                   # Type in your name
  author_email = 'deweshagrl2001@gmail.com',      # Type in your E-Mail
  keywords = ['PYTHON', 'TOPSIS', 'WEIGHTS','IMPACTS'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'Numpy',
          'Pandas',
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