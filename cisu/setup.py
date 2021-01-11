from setuptools import setup, find_packages


import os
the_lib_folder = os.path.dirname(os.path.realpath(__file__))
requirementPath = the_lib_folder + '/requirements.txt'
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

setup(
    name='cisu_python',
    version='0.1',
    packages=find_packages('src/'),
    package_dir={'cisu': 'src/cisu'},
    include_package_data=True,
    package_data={'cisu': [
        'constants/*.json',
        'templates/*.xml',
    ]},
    install_requires=install_requires,
)