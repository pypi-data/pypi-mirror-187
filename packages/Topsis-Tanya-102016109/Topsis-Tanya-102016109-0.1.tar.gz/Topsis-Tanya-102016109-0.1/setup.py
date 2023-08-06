
import os
import setuptools
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()
setuptools.setup( name='Topsis-Tanya-102016109', version='0.1', author="Tanya", author_email="tgarg1_be20@thapar.edu", description="Topsis", packages=setuptools.find_packages(),long_description=read('README.md'),long_description_content_type='text/markdown', classifiers=[ "Programming Language :: Python :: 3", "License :: OSI Approved :: MIT License", "Operating System :: OS Independent" ])