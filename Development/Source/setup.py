from setuptools import setup

setup(name='tapestry',
      version='2.1.1.20201230',
      description='tapestry development build - not suitable for release',
      author='Zac Adam-MacEwen',
      author_email='zadammac@kenshosec.com',
      url='https://www.github.com/zadammac/Tapestry',
      packages=['tapestry'],
      install_requires=['pysftp', 'python-gnupg', 'paramiko'],
     )
1