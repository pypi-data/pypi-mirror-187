from setuptools import setup, find_packages
import codecs
import os

setup(
    name="Topsis-Shreya-102016090", 
    version="0.0.4",
    license='MIT', 
    author="Shreya Saxena",
    author_email="shreyasaxena410@gmail.com",
    description="Topsis package for MCDM problems",
    url="https://pypi.python.org/pypi/Topsis-Shreya-102016090",
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
    ],
    entry_points={
        'console_scripts': [
            'topsis=topsis.main_102016090:topsis'
        ]
    },
    keywords=['python', 'TOPSIS', 'MCDM', 'MCDA',
              'statistics', 'prescriptive analytics', 'cli'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)