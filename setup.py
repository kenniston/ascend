from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='ascend',
    version='0.0.1',
    author='ASCEND Group',
    author_email='ascend@ita.br',
    url='ita.br',
    license='BSD',
    description='ASCEND research functions and algorithms.',
    # Long description read from the the readme file
    long_description=long_description,
    long_description_content_type='text/markdown',
    # List of all python modules to be installed
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Scientific/Engineering:: Artificial Intelligence',
        'Security',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[]
)
