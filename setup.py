import os, sys

from setuptools import setup, find_packages
from setuptools.command.install import install

script_path = os.path.join(sys.prefix, 'bin')

with open("README.md", "r") as fh:
    long_description = fh.read()


class PostInstallCommand(install):
    def run(self):
        os.system('chmod +x ' + os.path.join(script_path, 'Tres.py'))
        install.run(self)

setup(
    name="Tres",
    version="0.0.1",
    author="Peng Jiang",
    author_email="peng.jiang@nih.gov",
    description="Tumor-resilient T-cell model",
    
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    url="https://github.com/data2intelligence/Tres",
    
    packages=find_packages(),
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    
    python_requires = '>=3.6',
    
    install_requires=[
        'numpy',
        'pandas',
        'ridge_significance',
        'CytoSig',
    ],
    
    data_files=[
        ('bin', [
            os.path.join('src', 'Tres.py'),
            os.path.join('src', 'Tres.prediction_signature.gz'),
            os.path.join('src', 'Tres.kegg'),
            ]),
    ],
    
    cmdclass={
        'install': PostInstallCommand,
    },
)
