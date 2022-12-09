# -*- coding: utf-8 -*-

import setuptools


setuptools.setup(
    name="apika",
    version="0.1.2",
    author="huihui",
    author_email="sunjiehuimail@foxmail.com",
    description="aio pika",
    long_description="aio pika",
    long_description_content_type="text/markdown",
    url="https://github.com/JiehuiSun/apika",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Framework :: AsyncIO"
    ],
    install_requires=[
        "aio_pika==8.2.0"
    ],
    python_requires=">=3.8"

)
