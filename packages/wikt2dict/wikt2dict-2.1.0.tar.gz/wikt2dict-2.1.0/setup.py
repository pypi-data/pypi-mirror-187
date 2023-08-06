from setuptools import setup, find_packages
from glob import glob

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
import os
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install
from shutil import copyfile
from distutils.dir_util import copy_tree

HERE = os.path.abspath(os.path.dirname(__file__))
NAME = 'wikt2dict'

def copy_files (target_path):
    source_path = os.path.join(HERE)
    for fn in ["res"]:
        copy_tree(os.path.join(source_path, fn), os.path.join(target_path,fn))
    for fn in ["setup.py", "README.md"]:
        copyfile(os.path.join(source_path, fn), os.path.join(target_path,fn))

class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        develop.run(self)
        copy_files (os.path.abspath(NAME))

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        copy_files (os.path.abspath(os.path.join(self.install_lib)))

setup(
    author='Endre Hamerlik, Judit Acs',
    author_email='endre.hamerlik@fmph.uniba.sk, judit@sch.bme.hu',
    name=NAME,
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
    version='2.1.0', 
    provides=['wikt2dict'],
    url='https://github.com/HMRLKE/wikt2dict',
    #packages=['wikt2dict'],
    packages=find_packages(),
    package_dir={'': '.'},
    #package_data={"res":["langnames/*", "*.py"]},
    #package_data={'': ['res/*.tsv']},
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=['docopt'],
    scripts=['wikt2dict/w2d.py'],
    classifiers=[
        'Programming Language :: Python :: 3.8',
    ],
    data_files=[
        ('res', glob('res/langnames/*')),
        ('res', glob('res/wik*')),
        ('bin', glob('bin/*.py')),
        ('', glob('*yml')),
        #('w2d_env', glob('w2d_env/*')),
        ('wikt2dict/external', glob('wikt2dict/external/*.py'))
    ],
    
    description="""Wiktionary translation parser tool for many language editions.
    Wikt2dict parses only the translation sections.
    It also has a triangulation mode which combines the extracted translation pairs to generate new ones.""",
    long_description=long_description,
    long_description_content_type='text/markdown'
)
