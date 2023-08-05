#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="Autor",
    version="0.0.2",
    keywords=["pip", "Autor"],
    description="An application that helps you with your Hangzhou Safety Education Tasks",
    long_description="An application that helps you with your Hangzhou Safety Education Tasks",
    license="MIT Licence",

    url="https://github.com/7emotions/Autor",
    author="Lorenzo Feng",
    author_email="paradise_c@qq.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["selenium"]
)
