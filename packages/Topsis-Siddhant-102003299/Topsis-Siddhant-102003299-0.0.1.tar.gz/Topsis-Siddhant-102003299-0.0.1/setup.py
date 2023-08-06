from distutils.core import setup
import setuptools

setup(
  name = 'Topsis-Siddhant-102003299',
  packages = ['Topsis-Siddhant-102003299'],
  version = '0.0.1',
  license='MIT',
  description = 'This is a package for python where user has to input the csv file and weight and impacts and get the topsis ranking as a csv file output',
  author = 'Siddhant Aggarwal',
  author_email = 'saggarwal3_be20@thapar.edu',
  url = 'https://github.com/Siddhant2512/102003299-siddhant-topsis',
  keywords = ['Topsis', 'Ranking',],
  install_requires=[
          'pandas',
          'numpy',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)