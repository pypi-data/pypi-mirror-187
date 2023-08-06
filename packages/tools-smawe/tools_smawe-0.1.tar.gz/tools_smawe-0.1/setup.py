# -*- coding: utf-8 -*-
# @Author  : Smawe
# @Time    : 2023/1/17 19:11
# @File    : setup.py
# @Software: PyCharm

from setuptools import find_packages, setup


with open("README.md", "r", encoding="utf-8") as fp:
    LONG_DESCRIPTION = fp.read()

NAME = 'tools_smawe'
DESCRIPTION = 'small tool'
EMAIL = '1281722462@qq.com'
AUTHOR = 'Samwe'
REQUIRES_PYTHON = '>=3.5.0'
REQUIRED = ['lxml']

about = {"__version__": "0.1"}


setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    packages=find_packages(exclude=('tests',)),
    install_requires=REQUIRED,
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ]
)
