from distutils.core import setup


def readme():
    with open('README.md') as file:
        README = file.read()
    return README


setup(
    name='Topsis-Abhishek-102003364',
    packages=['Topsis-Abhishek-102003364'],
    version='0.1',
    license='MIT',
    description='This package can be used for implementation of Multiple criteria decision making using Topsis Algorithm. This is a python library for dealing with Multi-Criteria Decision Making (MCDM) problems by using techniques for order of preference by similarity to ideal solution (TOPSIS).',
    long_description=readme(),
    long_description_content_type="text/markdown",
    author='Abhishek Gandhi',
    author_email='abhishekgandhi989@gmail.com',
    url='https://github.com/Abhishek3450/topsis-package',
    download_url='https://github.com/Abhishek3450/topsis-package/archive/refs/tags/py.tar.gz',
    keywords=['topsis', 'multiple criteria decision'],
    install_requires=[
        'tabulate',
        'os',
        'pandas',
        'math',
        'sys'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
)
