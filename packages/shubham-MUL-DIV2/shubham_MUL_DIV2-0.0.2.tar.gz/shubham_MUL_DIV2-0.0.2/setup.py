
from setuptools import setup,find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Operating System :: Microsoft::Windows::Windows 10',
    'License :: OSI Approved :: MIT license',
    'Programming Language :: Python :: 3'
]

setup(
    name='shubham_MUL_DIV2',
    version='0.0.2',
    description='multiply and divide',
    long_description=open('README.txt').read()+'\n\n'+open('CHANGELOG.txt').read(),
    url='',
    author='Shubham Sahu',
    author_email='shubham30sahu101@gmail.com',
    keywords='muldiv',
    packages=find_packages(),
    install_requires = ['']
)