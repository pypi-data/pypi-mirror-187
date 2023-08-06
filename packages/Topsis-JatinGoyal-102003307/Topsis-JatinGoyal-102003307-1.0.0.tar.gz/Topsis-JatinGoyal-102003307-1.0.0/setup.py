from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name="Topsis-JatinGoyal-102003307",
    version="1.0.0",
    description="A Python package implementing TOPSIS technique.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/jating05/topsisImplementation",
    author="Jatin Goyal",
    author_email="jatingoyal452002@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["topsis"],
    include_package_data=True,
    install_requires=['numpy',
                      'pandas'
     ],
    entry_points={
        "console_scripts": [
            "topsis=topsis.__main__:main",
        ]
    },
)