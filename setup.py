import os
from setuptools import find_packages, setup
from colorfultable import author, author_email, name, version, website1

description = 'A module to help print beautiful table on the terminal.'
try:
    with open('README.md', 'r', encoding='utf-8') as mdfile:
        long_description = mdfile.read()
except:
    long_description = description

install_requires = ['colorama>=0.4.3'] if os.name == 'nt' else None

setup(
    name=name,
    version=version,
    author=author,
    author_email=author_email,
    maintainer=author,
    maintainer_email=author_email,
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT License',
    packages=find_packages(),
    platforms='any',
    url=website1,
    python_requires='>=3.5',
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords=['colorful', 'table', 'terminal', 'console', 'text'],
)
