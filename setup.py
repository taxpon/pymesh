from setuptools import setup
import pymesh

setup(
    name=pymesh.__title__,
    packages=[pymesh.__title__],
    version=pymesh.__version__,
    author=pymesh.__author__,
    author_email="taxpon@gmail.com",
    description="Library for manipulating (Translate, Rotate and Scale) 3D data using numpy.",
    url=pymesh.__url__,
    license=pymesh.__license__,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python",

    ],
    install_requires=[
        'numpy'
    ],
)
