from setuptools import setup, find_packages

setup(name='skoob-cli',
      version='1.0.0',
      packages=find_packages(),
      install_requires=['Click', 'requests', 'parsel'],
      include_package_data=True,
      entry_points={'console_scripts': ['skoob = src.interface:cli']})
