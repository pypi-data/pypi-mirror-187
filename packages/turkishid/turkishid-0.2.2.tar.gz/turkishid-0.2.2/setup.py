from setuptools import setup, find_packages


setup (
    name='turkishid',
    version='0.2.2',
    license='MIT',
    author="Onur Ravli",
    author_email='onur@ravli.co',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    description='Republic of Turkey Identity Number Validator.',
    url='https://github.com/onurravli/turkishid',
    keywords='turkishid'
)