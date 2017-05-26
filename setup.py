from setuptools import find_packages, setup

setup(
    name="enasearch",
    version="0.0.3",
    author="Berenice Batut",
    author_email="berenice.batut@gmail.com",
    description=("A Python library for interacting with ENA's API"),
    license="MIT",
    keywords="api api-client ena",
    url="https://github.com/bebatut/enasearch",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'enasearch = enasearch.__main__:main'
        ]
      },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Web Environment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6"
    ],
    extras_require={
        'testing': ["pytest"],
    },
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    install_requires=[
        'requests',
        'Click',
        'flake8',
        'xmltodict',
        'biopython'],
    include_package_data=True,
    package_data={'enasearch_data': ['enasearch_data/*.p']}
)
