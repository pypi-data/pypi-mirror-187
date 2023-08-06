from setuptools import setup,find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="Topsis-Girish-102003323",
    version="0.1.5",
    license='MIT',
    author="Girish Gupta",
    author_email="girish2001gupta@gmail.com",
    description="This package can be used to calculate the topsis score of multiple component data and rank them accordingly",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    keywords = ['TOPSIS'],  
    install_requires=[           
          'pandas',
          'numpy',
          'sklearn'
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3',     
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={
        'console_scripts': [
            'topsis=topsis.topsis:main'
        ]
    },
    project_urls={
        'Source': "https://github.com/girishnaman/topsis-package"
    },
) 
