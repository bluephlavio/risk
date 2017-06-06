from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()

setup(
    name='risk',
    version='0.0.1',
    description='Model and statistically analyze Risk game.',
    long_description=long_description,
    author='Flavio Grandin',
    author_email='flavio.grandin@gmail.com',
    install_requires=[
        'numpy',
    ],
    include_package_data=True,
    license='MIT',
    url='https://github.com/bluePhlavio/risk',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        ],
    keywords='risk',
    packages=['risk'],
    entry_points={
    },
)


