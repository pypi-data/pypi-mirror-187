from setuptools import setup, find_packages
import codecs
import os

#change to dict
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'README.md'), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.14'
DESCRIPTION = "Simple debugger for small scripts, shows the line being executed, local vars ..."

# Setting up
setup(
    name="TinyTinyDebugger",
    version=VERSION,
    license='MIT',
    url = 'https://github.com/hansalemaos/TinyTinyDebugger',
    author="Johannes Fischer",
    author_email="<aulasparticularesdealemaosp@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    #packages=['copy_functions_and_more', 'cprinter', 'files_folders_with_timestamp', 'sleepchunk', 'tolerant_isinstance', 'windows_filepath'],
    keywords=['debugger', 'debugging'],
    classifiers=['Development Status :: 4 - Beta', 'Programming Language :: Python :: 3 :: Only', 'Programming Language :: Python :: 3.9', 'Topic :: Scientific/Engineering :: Visualization', 'Topic :: Software Development :: Libraries :: Python Modules', 'Topic :: Text Editors :: Text Processing', 'Topic :: Text Processing :: General', 'Topic :: Text Processing :: Indexing', 'Topic :: Text Processing :: Filters', 'Topic :: Utilities'],
    install_requires=['copy_functions_and_more', 'cprinter', 'files_folders_with_timestamp', 'sleepchunk', 'tolerant_isinstance', 'windows_filepath'],
    include_package_data=True
)
#python setup.py sdist bdist_wheel
#twine upload dist/*