from setuptools import setup, find_packages

setup(name='skoob-cli',
      version='1.0.0',
      packages=find_packages('src'),
      install_requires=['Click', 'requests', 'parsel'],
      entry_points={'console_scripts': ['skoob = src.interface:cli']})
