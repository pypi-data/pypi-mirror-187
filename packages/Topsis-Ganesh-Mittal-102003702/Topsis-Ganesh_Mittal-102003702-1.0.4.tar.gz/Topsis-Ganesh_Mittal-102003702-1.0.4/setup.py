from setuptools import setup, find_packages

with open('requirements.txt') as f: 
    requirements = f.readlines() 
# with open("README.md") as f:
#     long_description = f.read()

setup(
    name='Topsis-Ganesh_Mittal-102003702',
    version='1.0.4',
    author='Ganesh Mittal',
    author_email='gmittal_be20@thapar.edu',
    description='A package -> Calculates Topsis Score and Rank them accordingly',
    # long_description=long_description,
    # long_description_content_type='text/markdown',
    license='MIT',
    packages = find_packages(),
    entry_points={
        'console_scripts': [
            'topsis=Topsis_Ganesh_Mittal.topsis:main',
        ]
    },
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords ='python package Ganesh Mittal', 
    install_requires = requirements, 
    zip_safe = False
)