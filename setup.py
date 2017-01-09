from setuptools import setup, find_packages


setup(
    name='AutoUploaderGoogleDrive',
    version='0.0.4dev',
    packages=find_packages(),
    long_description=open('README.md').read(),
    install_requires=[
        "google-api-python-client >= 1.2",
        "oauth2client >= 4.0.0",
        "httplib2",
        "rarfile",
    ],
    entry_points={
      'console_scripts': [
          'AutoUploaderGoogleDrive = AutoUploaderGoogleDrive:main'
      ]
    }
)
