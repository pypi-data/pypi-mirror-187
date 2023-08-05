from setuptools import setup, find_packages


setup (
    name='turkishid',
    version='0.1.1',
    license='MIT',
    author="Onur Ravli",
    author_email='onur@ravli.co',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/onurravli/turkishid',
    keywords='turkishid'
)