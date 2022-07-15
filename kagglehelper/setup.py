from setuptools import setup

setup(name='kagglehelper',
version='1.0.1',
description='Browse and Download Kaggle Datasets using the helper functions',
url='https://github.com/shounak8/custom_packages.git',
author='Shounak Deshpande',
author_email='shounak.python@gmail.com',
license='MIT',
packages=['kagglehelper'],
install_requires=['kaggle', 'pandas'],
zip_safe=False)