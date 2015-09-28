from setuptools import setup
import pymesh

setup(
    name=pymesh.__title__,
    packages=[pymesh.__title__],
    version=pymesh.__version__,
    author=pymesh.__author__,
    author_email="taxpon@gmail.com",
    description="Simple mesh manipulation library",
    url="",
    license="MIT",
    classifiers=['License :: OSI Approved :: BSD License'],
    install_requires=[
        'numpy'
    ],
)
