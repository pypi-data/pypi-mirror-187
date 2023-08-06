import setuptools 
setuptools.setup(
     name='Topsis_Harshit_102003653',
     version='0.2',
     author="Harshit Sharma", 
     author_email="emailforharshit25@gmail.com", 
     description="Python program using TOPSIS to calculate ranks based on data, weights and impacts",
     long_description = open('README.md').read(), 
     packages=setuptools.find_packages(), 
     classifiers=[ 
        "Programming Language :: Python :: 3", 
        "License :: OSI Approved :: MIT License", 
        "Operating System :: OS Independent", 
    ], 
)