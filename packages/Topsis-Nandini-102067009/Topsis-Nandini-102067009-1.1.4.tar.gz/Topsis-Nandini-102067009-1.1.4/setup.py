from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(  
  name = 'Topsis-Nandini-102067009',
  packages = ['topsis'],
  version = '1.1.4',
  license='MIT',
  description = 'API and CLI tool to calculate Topsis, CLI tool inputs CSV/Excel files',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Nandini Mehta',
  author_email = 'mehtanandini684@gmail.com',
  url = 'https://github.com/NandiniMehta0603/Topsis',
  keywords = ['topsis', 'python', 'pypi', 'csv', 'xlsx', 'xls', 'cli'],
  install_requires=[
          'numpy',
          'pandas',
      ],
  entry_points={
    'console_scripts': [
      'topsis = topsis.topsis:main'
      ]
  },
)