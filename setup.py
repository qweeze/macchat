import codecs
import os
import re
from setuptools import setup


with codecs.open(os.path.join(os.path.abspath(os.path.dirname(
        __file__)), 'macchat', '__init__.py'), 'r', 'latin1') as fp:
    try:
        version = re.findall(
            r"^__version__ = '([^']+)'\r?$", fp.read(), re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')

setup(
    name='macchat',
    version=version,
    url='',
    license='MIT',
    author='qweeze',
    author_email='qweeeze@gmail.com',
    description='A simple broadcast ethernet messenger',
    packages=['macchat'],
    package_data={'macchat': ['.macchatrc']},
    entry_points='''
        [console_scripts]
        macchat=macchat.main:main
    ''',
    install_requires=[
        'six',
        'configobj',
        'prompt_toolkit==1.0.9',
        'pycrypto',
        'click==6.6',
        'scapy'
    ],
    classifiers=[
    ],
)