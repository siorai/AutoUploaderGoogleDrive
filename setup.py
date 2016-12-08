from setuptools import setup, find_packages


setup(
    name='AutoUpload',
    version='0.0.1dev',
    packages=find_packages(),
    long_description=open('README.md').read(),
    entry_points={
      'console_scripts': [
          'AutoUpload = AutoUpload:main',
      ]
    }
)
