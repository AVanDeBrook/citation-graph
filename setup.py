from setuptools import *

setup(
    name='citation-graph',
    version='0.2.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'bibtexparser',
        'pylatexenc'
    ]
)
