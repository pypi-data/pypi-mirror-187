from setuptools import setup, find_packages
import codecs
import os

#change to dict
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'README.md'), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.10'
DESCRIPTION = "Download sites with public proxies - threading"

# Setting up
setup(
    name="site2hdd",
    version=VERSION,
    license='MIT',
    url = 'https://github.com/hansalemaos/site2hdd',
    author="Johannes Fischer",
    author_email="<aulasparticularesdealemaosp@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    #packages=['a_pandas_ex_apply_ignore_exceptions', 'a_pandas_ex_horizontal_explode', 'cprinter', 'freeproxydownloader', 'kthread_sleep', 'pandas', 'regex', 'requests', 'threadingbatch', 'tolerant_isinstance', 'touchtouch', 'url_analyzer'],
    keywords=['download', 'scrape', 'site'],
    classifiers=['Development Status :: 4 - Beta', 'Programming Language :: Python :: 3 :: Only', 'Programming Language :: Python :: 3.9', 'Topic :: Scientific/Engineering :: Visualization', 'Topic :: Software Development :: Libraries :: Python Modules', 'Topic :: Text Editors :: Text Processing', 'Topic :: Text Processing :: General', 'Topic :: Text Processing :: Indexing', 'Topic :: Text Processing :: Filters', 'Topic :: Utilities'],
    install_requires=['a_pandas_ex_apply_ignore_exceptions', 'a_pandas_ex_horizontal_explode', 'cprinter', 'freeproxydownloader', 'kthread_sleep', 'pandas', 'regex', 'requests', 'threadingbatch', 'tolerant_isinstance', 'touchtouch', 'url_analyzer'],
    include_package_data=True
)
#python setup.py sdist bdist_wheel
#twine upload dist/*