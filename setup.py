#!/usr/bin/env python
from setuptools import setup, find_packages


def read(file_path):
    with open(file_path) as fp:
        return fp.read()


setup(
    name='docker-registry-purger',
    version='0.1.0',
    description="A simple docker registry cleaner",
    long_description=read('README.rst'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: System :: Software Distribution',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
    keywords=['docker', 'docker-registry', 'cleaner'],
    author='Polyconseil',
    author_email='opensource+docker-registry-purger@polyconseil.fr',
    url='https://github.com/Polyconseil/docker-registry-purger/',
    license='BSD',
    packages=find_packages(where='src'),
    package_dir={'': str('src')},
    include_package_data=True,
    zip_safe=False,
    setup_requires=[
        'setuptools',
    ],
    install_requires=[
        'click',
        'daiquiri',
        'isodate',
        'requests',
    ],
    entry_points={
        'console_scripts': (
            'docker-registry-purger = docker_registry_purger.__init__:main',
        ),
    },
)
