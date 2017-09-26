# -------------------------------------------------------------------
# - NAME:        setup.py
# - AUTHOR:      Reto Stauffer
# - DATE:        2017-02-05
# -------------------------------------------------------------------
# - DESCRIPTION: Installer for the PySweave python binary (It's
#                actually only a binary at the end).
# -------------------------------------------------------------------
# - EDITORIAL:   2017-02-05, RS: Created file on thinkreto.
# -------------------------------------------------------------------
# - L@ST MODIFIED: 2017-09-26 12:08 on thinkreto
# -------------------------------------------------------------------
from setuptools import setup

setup(name='PySweave',     # This is the package name
      version='0.0-1',            # Current package version, what else
      description='Small python sweaver script',
      long_description='No long description necessary',
      classifiers=[
        'Development Status :: 3 - Alpha',
        #'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2.7',
      ],
      keywords='beamer sweave latex Rnw',
      url='https://github.com/retostauffer/PySweave',
      author='Reto Stauffer',
      author_email='reto.stauffer@uibk.ac.at',
      license='GPL-2',
      packages=['PySweave'],
      install_requires=[
         'logging',
      ],
      scripts=['bin/PySweave'],
      include_package_data=True,
      czip_safe=False)

