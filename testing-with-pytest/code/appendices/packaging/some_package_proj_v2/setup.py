from setuptools import setup, find_packages

setup(
    name='some_package',
    description='Demonstrate packaging and distribution',

    version='1.0',
    author='Fenago',
    author_email='brian@pythontesting.net',
    url='https://pragprog.com/book/bopytest/python-testing-with-pytest',

    packages=find_packages(where='src'),
    package_dir={'': 'src'},
)
