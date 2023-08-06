from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'This program uses command line arguments to implement Topsis : a Multi-Criteria Decision Ananlysis (MCDA) method'
with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

# Setting up
setup(
    name="topsis-Ananya-102017024", 
    version=VERSION,
    author="Ananya Thomas",
    author_email="ananyathomas10@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['numpy','pandas'], 
    entry_points={
        'console_scripts': [
        'topsis=topsis.topsis:main'
        ]
    },
    keywords=['python', 'TOPSIS' ,'MCDA', 'MCDM','predictive analytics','statistics'],
    classifiers= [
        "Intended Audience :: Information Technology",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
