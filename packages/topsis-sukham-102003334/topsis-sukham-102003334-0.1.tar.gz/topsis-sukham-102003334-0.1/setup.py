from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name="topsis-sukham-102003334",
    version="0.1",
    description="A Python package implementing TOPSIS technique.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Sukham",
    author_email="schatha_be20@thapar.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["topsis_sukham_102003334"],
    include_package_data=True,
    install_requires=[
                      'numpy',
                      'pandas'
     ],
     entry_points={
        "console_scripts": [
            "topsispy=topsis_sukham_102003334.topsis:main",
        ]
     },
)
