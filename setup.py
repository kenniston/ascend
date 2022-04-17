from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='ascendcontroller',
    version='0.0.1',
    author='ASCEND Controller Group',
    author_email='ascend-controller@ita.br',
    url='ita.br',
    license='BSD',
    description='ASCEND Controller research functions and algorithms.',
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
    install_requires=[
        'pandas>=1.4.2',
        'typing_extensions>=4.1.1',
        'scipy>=1.8.0',
        'ipykernel>=6.13.0',
        'matplotlib>=3.5.1'
    ]
)
