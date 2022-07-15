from setuptools import setup

setup(name='kagglehelper1',
version='1.0.0',
description='Browse and Download Kaggle Datasets using the helper functions',
url='https://github.com/shounak8/custom_packages/tree/master/kagglehelper',
author='Shounak Deshpande',
author_email='shounak.python@gmail.com',
license='MIT',
packages=['kagglehelper1'],
install_requires=['kaggle', 'pandas'],
zip_safe=False)