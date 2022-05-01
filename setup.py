# Original Author: Codec04
# Re-built by Itz-fork
# Project: Gofile2
import os

from re import findall
from setuptools import setup, find_packages

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


# Requirements
if os.path.isfile('requirements.txt'):
    with open('requirements.txt') as req:
        reques = req.read().splitlines()
else:
    reques = [
        'requests',
        'aiohttp'
    ]

# Readme
if os.path.isfile('README.md'):
    with open(('README.md'), encoding='utf-8') as readmeh:
        big_description = readmeh.read()
else:
    big_description = "Gofile2 is an API wrapper for Gofile API"

# Version (https://github.com/pyrogram/pyrogram/blob/97b6c32c7ff707fd2721338581e7dad5072f745e/setup.py#L30)
with open("gofile2/__init__.py", encoding="utf-8") as f:
    v = findall(r"__version__ = \"(.+)\"", f.read())[0]


setup(name='gofile2',
      version=v,
      description='An API wrapper for Gofile API',
      url='https://github.com/Itz-fork/Gofile2',
      author='Itz-fork, Codec04',
      author_email='itz-fork@users.noreply.github.com',
      license='MIT',
      packages=find_packages(),
      download_url=f"https://github.com/Itz-fork/Gofile2/releases/tag/Gofile2-{v}",
      keywords=['Gofile', 'Api-wrapper', 'Gofile2'],
      long_description=big_description,
      long_description_content_type='text/markdown',
      install_requires=reques,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Topic :: Education',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.9',
      ],
      )
