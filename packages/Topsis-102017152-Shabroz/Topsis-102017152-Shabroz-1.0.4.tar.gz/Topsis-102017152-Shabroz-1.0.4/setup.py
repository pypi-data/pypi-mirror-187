from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

setup(
    name='Topsis-102017152-Shabroz',
    version='1.0.4',
    author='Shabroz Kaur',
    author_email='skaur2_be20@thapar.edu',
    description="A package -> Calculates Topsis Score and Rank them accordingly",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=["code"],
    include_package_data=True,
    install_requires='panda',
    entry_points={
        'console_scripts': [
            'topsis=topsis.102017152:main',
        ]
    },
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='python package ShabrozKaur',

)