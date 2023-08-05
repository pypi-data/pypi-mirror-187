from distutils.core import setup
setup(
  name = 'packagetest311110',         # How you named your package folder (MyLib)
  packages = ['packagetest311110'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This is test package',   # Give a short description about your library
  author = 'testuser',                   # Type in your name
  author_email = 'rodiksha218@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/Dik17/PackageTest311110',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Dik17/PackageTest311110/archive/refs/tags/v_01.tar.gz',    # I explain this later on
  keywords = ['SOME', '311110', 'TOPSIS'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas',
          'numpy',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
 
  ],
)