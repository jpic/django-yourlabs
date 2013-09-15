import os
import sys

from setuptools import setup, find_packages

version = __import__('yourlabs').VERSION


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='django-yourlabs',
    version=version,
    description='Fresh Django starter project and helpers',
    author='James Pic',
    author_email='jamespic@gmail.com',
    url='http://django-yourlabs.rtfd.org',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    scripts=['yourlabs/bin/yl'],
    long_description=read('README.rst'),
    license='MIT',
    keywords='django template starter',
    install_requires=[
        'django',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
