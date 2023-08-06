from setuptools import setup,find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Operating System :: Microsoft::Windows::Windows 10',
    'License :: OSI Approved :: MIT license',
    'Programming Language :: Python :: 3'
]

setup(
    name='Topsis-Shubham-102067011',
    version='0.0.1',
    description='TOPSIS for MCDM(Multiple Criteria Decision Making)',
    long_description=open('README.txt').read()+'\n\n'+open('CHANGELOG.txt').read(),
    url='',
    author='Shubham Sahu',
    author_email='shubham30sahu101@gmail.com',
    keywords='TOPSIS',
    packages=find_packages(),
    install_requires = ['numpy']
)