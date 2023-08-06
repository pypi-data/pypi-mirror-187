from pathlib import Path

from setuptools import setup, find_packages

# install_requires = (Path(__file__).parent / 'requirements.txt').read_text().split('\n')

setup(
    name='pynanto',
    version='0.1.1',
    packages=find_packages(include=['pynanto', 'pynanto.*', 'js', 'js.*']),
    package_data={'js': ['__init__.pyi'], 'pynanto': ['bootstrap_pyodide.js']},
    # install_requires=install_requires,
    classifiers=[
    ],
)
