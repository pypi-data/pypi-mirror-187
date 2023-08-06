from setuptools import setup, find_packages

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name='Calculator22BEE0032',
    version='0.1',
    summary='A package that adds 2 numbers',
    package_dir={'': 'Calculator22BEE0032'},
    packages=find_packages('Calculator22BEE0032'),
    install_requires=[],
    author='Tanishka Gaur',
    author_email='tanishkagaur9211@gmail.com',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
    license='MIT',
    python_requires='>=3.7',
    keywords='calculator',
    description='A simple calculator package',
    long_description=long_description,
    long_description_content_type="text/x-rst",
)
