import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='sympy-slider',
    version='0.0.1',
    author='Bryan Fichera',
    author_email='bfichera@mit.edu',
    description='Make slider from sympy expression and params',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/bfichera/sympy-slider',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'sympy',
        'numpy',
        'matplotlib',
    ]
)
