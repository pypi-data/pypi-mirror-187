from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name='Topsis-Sailish-102003768',
    version='1.0.0',
    description='A TOPSIS calculator',
    long_description = readme(),
    long_description_content_type = "text/markdown",
    url='',  
    author='Sailish Makkar',
    author_email='smakkar_be20@thapar.edu',
    license='MIT',
    keywords='TOPSIS',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'topsis=topsis.topsis:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",        
    ],
)